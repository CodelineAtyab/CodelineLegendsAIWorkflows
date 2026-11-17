# Star Wars Dossier with Temporal (issue #295)

A Temporal workflow that builds a character dossier from [SWAPI](https://swapi.dev/) using
**dependent** requests: search for the character, then use the URLs in that response to fetch the
homeworld and the film titles.

```
starter.py ──► Temporal server (Docker, Postgres) ──► worker.py
                                                       ├─ find_character   GET /people/?search=<name>
                                                       ├─ get_homeworld    GET <homeworld URL from step 1>
                                                       └─ get_film (×N)    GET <each film URL from step 1>
```

| File | Role |
|---|---|
| `docker-compose.yml` | Postgres + Temporal server + Web UI |
| `activities.py` | One HTTP request per activity; classifies errors as retryable or not |
| `workflows.py` | Deterministic recipe: calls the activities in order with a retry policy |
| `worker.py` | Polls the `star-wars-dossier` task queue and runs the code |
| `starter.py` | Starts a workflow for a name and prints the dossier as JSON |
| `shared.py` | Task queue name, Temporal address, workflow input dataclass |

## Run it

```bash
cp .env.example .env          # then change POSTGRES_PASSWORD
docker compose up -d          # UI: http://localhost:8080
uv run worker.py              # terminal 1
uv run starter.py "Luke Skywalker"   # terminal 2
```

Output:

```json
{
  "name": "Luke Skywalker",
  "homeworld": "Tatooine",
  "films": ["A New Hope", "The Empire Strikes Back", "Return of the Jedi", "Revenge of the Sith"]
}
```

`uv run starter.py "Nobody McNobody"` prints `Error: Character not found: 'Nobody McNobody'` and
exits with code 1 after a **single** attempt (the error is non-retryable).

## Error handling

| Situation | What happens |
|---|---|
| No search result | `CharacterNotFound`, non-retryable → workflow fails at once |
| Other 4xx (e.g. 404) | non-retryable: asking again returns the same answer |
| Network error, timeout, 5xx, 408, 429 | retried: 1s, 2s, 4s … (max 30s between attempts), up to 10 attempts |

## Proving durability

**Retry test**: start the worker with a broken URL, start a workflow, watch the retries in the UI,
then fix the worker. The *same* workflow completes without being restarted.

```bash
SWAPI_BASE_URL=https://swapi.invalid/api uv run worker.py   # broken worker (PowerShell: $env:SWAPI_BASE_URL="...")
uv run starter.py "Han Solo"                                 # UI shows find_character attempt 2, 3, 4 ...
# Ctrl+C the broken worker, then start a normal one:
uv run worker.py                                             # starter prints the dossier
```

**Worker-crash test**: `--step-delay` adds a durable `workflow.sleep` between steps, so there is
time to kill the worker mid-way.

```bash
uv run worker.py
uv run starter.py "Leia Organa" --step-delay 15
# after "Searching for character" appears in the worker log, Ctrl+C the worker, wait, start it again
uv run worker.py
```

The second worker does **not** search for the character again: the result of `find_character` is
already in the workflow history, so it continues with `get_homeworld`. You can see this in the
UI event history (only one `ActivityTaskCompleted` for `find_character`).

Both tests were run locally while building this. **Add the screenshots from the UI to the PR.**

## Responsible AI use

### Tool and prompts

<!-- TODO (Louai): rewrite in your own words — what you actually typed. -->
Tool: Claude Code. Prompts, in order:
1. "Read issue #295 and explain what it asks for."
2. "Write the docker-compose.yml for Temporal + Postgres + UI with a health check and a named volume."
3. "Write the activities, one HTTP request each, with a non-retryable not-found error."
4. "Write the workflow, worker and starter; then run the retry test and the crash test."

### Three things the AI got wrong / that I changed

<!-- TODO (Louai): review and replace with your own observations. -->
1. **Film fetching in one activity.** The first idea was a single `get_films` activity that loops
   over all URLs. That breaks the "one request per activity" rule and means one failing film
   re-fetches all of them. Changed to one `get_film` activity per URL, run in parallel.
2. **Dossier key order.** Temporal's JSON converter sorts dict keys, so the output came out as
   `films, homeworld, name`. `starter.py` now rebuilds the dict in the required order.
3. **Killing the worker during testing.** The AI's first command to kill the worker used a filter
   that would have killed far more processes than just the worker. It was blocked, and the
   command was narrowed to match only `worker.py`. Lesson: read commands before running them.

### What Temporal saved me from

<!-- TODO (Louai): write this paragraph yourself — this is the graded part. -->
_Write here, in your own words: without Temporal I would have had to write my own retry loop with
backoff, decide which errors are worth retrying, and save each step's result somewhere (a file or
DB) so a crash doesn't force restarting from the search. With Temporal the history in Postgres is
that "save progress", the retry policy is configuration, and a killed worker just resumes._
