# Star Wars Dossier (Temporal practice)

Issue #295: Practising AI-Driven Development with Temporal, Docker Compose and
dependent API requests.

Give it a Star Wars character name. A Temporal workflow then builds a small
dossier from [SWAPI](https://swapi.dev/) using **dependent** requests: it finds
the character first, then uses the URLs from that answer to fetch the homeworld
and the films.

```json
{
  "name": "Luke Skywalker",
  "homeworld": "Tatooine",
  "films": ["A New Hope", "The Empire Strikes Back", "Return of the Jedi", "Revenge of the Sith"]
}
```

## Files

| File | Purpose |
|------|---------|
| `main.py` | Tiny check that SWAPI is reachable (no Temporal). |
| `docker-compose.yml` | Temporal server + Postgres + Web UI (pinned versions). |
| `.env.example` | Which credentials `.env` needs (placeholders only). |
| `activities.py` | The 3 steps that call SWAPI: `find_character`, `get_homeworld`, `get_films`. |
| `workflows.py` | `DossierWorkflow`: calls the activities in order, with timeouts and retries. |
| `worker.py` | Runs the workflow and activities on task queue `star-wars-dossier`. |
| `starter.py` | Starts a workflow for a name and prints the dossier. |

## How to run

You need Docker Desktop and [uv](https://docs.astral.sh/uv/).

```bash
# 1. Create your local credentials file (once), then edit the values
cp .env.example .env

# 2. Start Temporal + Postgres + Web UI (UI on http://localhost:8080)
docker compose up -d

# 3. In terminal 1: start the worker and leave it running
uv run worker.py

# 4. In terminal 2: build a dossier
uv run starter.py "Luke Skywalker"
uv run starter.py "Nobody McNobody"   # -> Error: Character not found: Nobody McNobody
```

Stop everything with `Ctrl+C` in the worker terminal and `docker compose down`
(add `-v` only if you also want to delete the database volume).

## Tools and prompts

I used **Claude Code** (an AI coding assistant) for this exercise. Summary of my prompt:

- Build a Temporal workflow that turns a Star Wars character name into a dossier
  (name, homeworld, films) using dependent SWAPI requests, as three activities.
- Run Temporal + Postgres + Web UI with Docker Compose: pinned image versions,
  named volume, Postgres health check, credentials from `.env`.
- Retries with backoff for network/5xx errors; "character not found" is non-retryable.
- Simple beginner code with comments that explain *why*; check the real Temporal
  docs instead of guessing; verify both the happy path and the not-found path,
  and pass the repo's ruff and mypy checks.

## Three things the AI got wrong or that I changed

- **The official Temporal docker-compose file did not meet the issue's
  requirements.** It used an anonymous volume instead of a named one, had no
  health checks, used plain `depends_on`, hard-coded the `temporal/temporal`
  credentials, and added an extra admin-tools container and an exposed Postgres
  port. I trimmed it down and fixed these points: a named volume, a Postgres
  health check that Temporal waits for, and credentials read from `.env`.
- **The dossier came back in the wrong order.** Temporal's JSON converter sorts
  dict keys, so the result was `films`, `homeworld`, `name` instead of `name`,
  `homeworld`, `films`. I changed `starter.py` to put the keys back in a
  reader-friendly order before printing.
- **My first retry test ran out of attempts.** With `maximum_attempts=8` the
  retries only last about 2 minutes, and that was not enough time to fix the
  code, so the workflow failed (`dossier-luke-skywalker-64bafd89`). I raised
  `maximum_attempts` to 20 just for the test, then set it back to 8.

## What Temporal saved me from

<!-- Draft by Claude Code; reviewed and edited by Mohammed -->
Without Temporal I would have had to write my own retry loop, with delays
between tries and a maximum number of attempts. I would also have had to save
the result of each step somewhere, so that a crash would not force me to start
again from step 1. In my retry test, `get_homeworld` failed 17 times and
succeeded on attempt 18, in the SAME workflow, without running the starter
again. In my crash test, I killed the worker during `get_films`, and a new
worker process finished it, while `find_character` and `get_homeworld` were not
run again. My workflow code stays simple because Temporal handles the retries
and remembers the progress for me.

## Durability tests

### Retry test

Workflow: `dossier-luke-skywalker-08147233`

I broke `get_homeworld` on purpose by adding `"broken/"` to the URL, so SWAPI
returned 404. I also raised `maximum_attempts` to 20 for this test only. In the
Temporal UI, Pending Activities showed the attempt count of `get_homeworld`
going up with the 404 error, while `find_character` had already completed once
(attempt 1). Then I fixed the code and restarted only the worker, without
running the starter again. The same workflow completed: `get_homeworld`
succeeded on attempt 18. `find_character` was run by worker process 24416, and
`get_homeworld` attempt 18 by process 28392. Total time: 7m 13s.

Screenshots: see the pull request description.

### Worker-crash test

Workflow: `dossier-luke-skywalker-86a05fb8`

I added a temporary 20-second sleep in `get_films` to have time to crash it.
4 seconds after `get_films` started, I killed the worker hard
(`taskkill /F`, PID 25224), then started it again. Temporal timed out the lost
attempt after 30 seconds, and `get_films` completed on attempt 2 on the new
worker (PID 51604). `find_character` and `get_homeworld` show only one
completion each (attempt 1), so they were not run again. The workflow
completed in 34.8s.

Screenshots: see the pull request description.
