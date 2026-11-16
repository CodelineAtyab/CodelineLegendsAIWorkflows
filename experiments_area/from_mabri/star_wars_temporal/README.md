# Star Wars Dossier with Temporal

Issue #295. Given a character name, a durable [Temporal](https://temporal.io/) workflow
builds a dossier from **dependent** requests to the [Star Wars API](https://swapi.dev/):
search for the character, then follow the URLs in that result to get the
homeworld, every film and (if there is one) the species.

```json
{
  "name": "Luke Skywalker",
  "homeworld": "Tatooine",
  "films": ["A New Hope", "The Empire Strikes Back", "Return of the Jedi", "Revenge of the Sith"]
}
```

## How it fits together

| File | Role |
|---|---|
| `docker-compose.yml` | Postgres (Temporal's database), Temporal server, Temporal Web UI |
| `activities.py` | The only place with HTTP calls. One request per activity: `find_character`, `get_homeworld`, `get_film`, `get_species` |
| `workflows.py` | `CharacterDossierWorkflow`: calls the activities in order, with a retry policy and timeouts. No HTTP, no randomness |
| `worker.py` | Runs the workflow and activities from task queue `star-wars-dossier` |
| `starter.py` | Starts one workflow and prints the dossier as JSON |
| `docs/DURABILITY.md` | Retry test and worker-crash test, with screenshots |

```
starter.py --start--> Temporal server (history in Postgres) <--poll-- worker.py
                                                                 |
             find_character -> get_homeworld -> get_film x N -> get_species
```

## Run it

You need Docker Desktop and [uv](https://docs.astral.sh/uv/).

1. Create your local settings (this file is git-ignored) and set a password in it:
   ```bash
   cp .env.example .env
   ```
2. Start Postgres, Temporal and the UI. `--wait` returns once all three are healthy:
   ```bash
   docker compose up -d --wait
   ```
   The UI is at http://localhost:8080 and shows the `default` namespace.
3. In one terminal, start the worker (Ctrl+C stops it):
   ```bash
   uv run worker.py
   ```
4. In a second terminal, ask for a dossier (with no name it defaults to Luke Skywalker):
   ```bash
   uv run starter.py "Luke Skywalker"
   ```
5. A name that does not exist fails at once with a clear message and exit code 1.
   It is not retried, because no retry can make a missing character appear:
   ```bash
   uv run starter.py "Nobody McNobody"
   ```
   ```
   Error: Character not found: 'Nobody McNobody'
   ```
   The worker terminal shows a traceback for this failure. That is the SDK
   logging the failed activity, not a crash.

Stop the stack with `docker compose down`. Workflow history is kept in the
`temporal_pg_data` volume. Use `docker compose down -v` to wipe it.

### Settings

| Variable | Default | Used for |
|---|---|---|
| `TEMPORAL_ADDRESS` | `localhost:7233` | Where `worker.py` and `starter.py` find the server |
| `SWAPI_BASE_URL` | `https://swapi.dev/api` | Set to a host that does not exist to break the search step (retry test) |
| `SLOW_FILM_SECONDS` | `0` | Pause inside each film step, giving time to kill the worker (crash test) |

## Error handling

| Failure | Retried? | Why |
|---|---|---|
| No search results | No (`CharacterNotFound`) | Retrying cannot change the answer |
| 4xx from SWAPI, except 429 | No (`SwapiClientError`) | The request itself is wrong |
| 429, 5xx, timeout, network error | Yes, up to 8 attempts (1s, 2s, 4s, 8s, 16s, then 30s waits) | Temporary problems that often go away |

## Durability

Both tests from the issue were run, and the full evidence is in
[docs/DURABILITY.md](docs/DURABILITY.md).

- **Retry test:** with SWAPI broken, `find_character` was retried automatically.
  After the fix it succeeded on attempt 6, in the same workflow run.
- **Worker-crash test:** the worker was force-killed after 2 of 4 films. A new
  worker finished the run and repeated only the film that was in progress.
  The search, the homeworld and the first two films were not run again.

## How AI was used

**Tool:** Claude Code (desktop app), working through the issue one step at a time,
with one commit per step and a review after each step.

**Prompts I used** (in order):

1. "let's take issue 295 step by step". Claude read the issue and proposed a 9-step plan, which I approved.
2. "commit for each step"
3. "Yes, Step N" after reviewing each step's result.
4. For Step 3, where the issue asks me to write the basic `fetch_json` function myself,
   I asked Claude to write it ("you do"). I then reviewed it line by line so I can explain it.

**Three things the AI got wrong, or that I changed:**

1. **The retry window was too short.** The first retry policy allowed 5 attempts,
   which is only about 15 seconds of retrying in total. That is too short for the
   issue's "fix it without restarting the workflow" test. It was raised to 8
   attempts, about 90 seconds in total.
2. **A config file was silently left out of a commit.** The repo-root `.gitignore`
   ignores every `dynamicconfig/` folder, so the first Docker Compose commit did not
   include the config file that the compose file mounts. A fresh clone would have
   started Temporal without it. This was caught by checking `git show --stat`
   after the commit, and fixed with `!dynamicconfig/` in this project's
   `.gitignore`. Lesson: check what a commit really contains.
3. **The dossier's key order didn't match.** Temporal's JSON converter sorts
   dictionary keys, so the dossier came back as `films, homeworld, name` instead of
   the issue's `name, homeworld, films`. `starter.py` now puts the keys back in the
   issue's order before printing.

## What Temporal saved me from

 As a developer Temporal saved me from writing and maintaining complex failure-handling, state-management, and retry boilerplate code in distributed systems.
