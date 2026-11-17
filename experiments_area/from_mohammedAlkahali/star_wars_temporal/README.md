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

- TODO (Mohammed)
- TODO (Mohammed)
- TODO (Mohammed)

## What Temporal saved me from

TODO (Mohammed, in my own words)

## Durability tests

### Retry test

TODO (Mohammed): notes on how I broke an activity, what the retries looked like,
and how the workflow completed after the fix.

<!-- Screenshot: activity retries (attempt count / last failure) in the Temporal UI -->
<!-- Screenshot: same workflow Completed after the fix -->

### Worker-crash test

TODO (Mohammed): notes on killing the worker mid-workflow and restarting it.

<!-- Screenshot: event history showing completed activities before the crash -->
<!-- Screenshot: workflow Completed, with earlier activities not run again -->
