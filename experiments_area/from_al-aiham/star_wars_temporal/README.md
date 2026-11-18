# Star Wars Temporal dossier

Build a character dossier through dependent SWAPI requests. Temporal stores each
completed activity result in Postgres, so a retry or replacement worker can
continue the same workflow.

## Run

Use Python 3.14, uv, and Docker Desktop with its Linux engine running. Run these
commands from this directory. On a fresh checkout, copy `.env.example` to `.env`
and choose a made-up local database password before starting the stack. The
local `.env` created during verification is already configured; keep its values
when reusing the existing database volume.

```powershell
docker compose up -d
```

The Web UI is at <http://localhost:8080>, in namespace `default`.
Leave the worker running in one terminal:

```powershell
uv run worker.py
```

In another terminal:

```powershell
uv run starter.py "Luke Skywalker"
uv run starter.py "Nobody McNobody"
```

The first command prints JSON with `name`, `homeworld`, and `films`. Omitting the
name defaults to Luke Skywalker. The second exits with status 1 and prints
`Character 'Nobody McNobody' was not found.` without retrying. The workflow ID
is printed to stderr so stdout remains JSON on success.

Stop the stack with `docker compose down`. Its named Postgres volume preserves
history for the next startup.

## Code and AI review

Tool: Codex desktop coding agent, using PowerShell, uv, and Docker CLI. Prompts
were split into the minimal three-service Compose stack, the three required
activities and deterministic workflow, then verification of retries and worker
replacement. No optional species activity was added.

Three changes made during review:

1. Corrected the Temporal health-check address from `127.0.0.1:7233` to
   `temporal:7233`: the container server binds its container address, so the old
   check incorrectly marked a running server unhealthy.
2. Made `get_films` fetch one film URL per invocation. The workflow collects
   titles in order, reconciling the film-list step with the requirement for one
   HTTP request per activity and preserving completed titles across failures.
3. Unwrapped nested workflow/activity failures in the starter so a missing
   character prints the underlying message rather than only "Activity task
   failed". Its `CharacterNotFound` error is explicitly non-retryable.

Temporal saved me from writing retry loops and intermediate-result files.
Only activities perform HTTP requests; the workflow records their order and
uses the character response to supply the homeworld and film URLs. On recovery,
Temporal replays the recorded results and schedules the unfinished activity,
instead of asking me to restart all requests from the beginning.

This is AI-assisted code, including the small HTTP helper. The exercise's
handwritten warm-up and personal ability to explain every line must be completed
by the submitting developer; this README does not attest that they happened.

## Durability evidence / PR notes

Verified locally on 17 November 2026 against the Compose stack and real SWAPI.
These notes can be copied into the PR description with `Closes #295`.

- **Normal run:** Luke returned `Tatooine` and the four film titles from SWAPI.
  The not-found workflow history showed exactly one activity attempt and a
  non-retryable failure.
- **Retry:** workflow `proof-retry-a10c2b39-fe36-42db-8c3d-24e7e6b97b7c`, run
  `01a1e83e-7f59-769f-ac32-6ba791316c8c`. A temporary, ignored verification
  worker redirected the homeworld request to a local endpoint that timed out.
  The UI showed `get_homeworld`, **Attempt 3 / 5**, while the workflow was
  Running. Removing that temporary fault let the same worker and workflow
  complete; the UI then showed Completed and the dossier. No manual workflow
  restart was used.
- **Worker crash:** workflow `proof-crash-ce5a2946-351a-4583-a590-d0df9ac2d594`,
  run `01a1e83f-3ad9-79a6-8016-4fc15768d427`. Worker PID 5320 was killed while
  `get_homeworld` was in progress, after `find_character` completed. The UI
  retained the Running workflow and pending activity. Production worker PID
  19664 resumed the same run, which the UI showed as Completed. History contains
  exactly one completed `find_character` before and after the crash, followed by
  one homeworld result and four film results.
- **Persistence:** after `docker compose down` and `docker compose up -d`, both
  proof runs were still Completed and returned their stored dossiers. The Web UI
  also responded successfully after the containers were recreated.

Temporary fault injection and verification scripts stay in ignored `.cache/`;
the submitted worker and activities contain no test switches or artificial delays.







docker compose up -d
uv run worker.py
uv run starter.py "Luke Skywalker"