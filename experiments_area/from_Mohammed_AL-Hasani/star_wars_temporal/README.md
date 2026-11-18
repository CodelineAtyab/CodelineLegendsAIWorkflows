# Star Wars Dossier (Temporal + Docker Compose)

A Temporal workflow that builds a Star Wars character dossier from three **dependent** SWAPI
requests: find the character, then fetch the homeworld and the films using URLs from step 1.

## Run it

```
cp .env.example .env            # choose your own local Postgres password
docker compose up -d            # Postgres, then Temporal, then the Web UI (http://localhost:8080)
uv run worker.py                # terminal 1: keeps running
uv run starter.py "Luke Skywalker"   # terminal 2: prints the dossier as JSON
uv run starter.py "Nobody McNobody"  # fails cleanly: "Character not found", no endless retries
docker compose down             # stop (workflow history stays in the named volume)
```

Files: `swapi_client.py` (plain HTTP helper), `activities.py` (the steps), `workflow.py` (the
recipe), `worker.py`, `starter.py`, `docker-compose.yml`.

## Tool and prompts

I used **Claude Code**. I gave it the issue text and asked it to build the project in small steps:
the Compose stack first (and to check it comes up healthy), then the HTTP helper and activities,
then the workflow, worker and starter, and finally to run the two durability tests and write down
the evidence. After each file I read it and checked the Temporal parts against how the SDK works
(sandbox imports, retry policy, non-retryable errors).

## Three things the AI got wrong or that I changed

1. **Result key order.** The first version returned a plain `dict`. Temporal's JSON encoding sorts
   dict keys alphabetically, so the output was `films, homeworld, name` instead of the
   `name, homeworld, films` format from the issue. I changed the workflow to return a small
   `Dossier` dataclass so the field order is fixed.
2. **My first crash test proved nothing.** The real steps finish in about a second, so by the time
   I killed the worker the workflow had already completed. I added an optional
   `ACTIVITY_PAUSE_SECONDS` setting (default `0`, only for demos) so each step is slow enough to
   kill the worker mid-way, and repeated the test.
3. **`get_films` makes several requests.** The issue says each activity makes one HTTP request,
   but step 3 needs one request per film. I kept one `get_films` activity (as in the issue's
   table) that sends the film requests together. The downside is that if one film request fails,
   the whole activity is retried. A fan-out with one activity per film would avoid that.

## What Temporal saved me from

Without Temporal, step 3 depends on step 2's data, so a failure late in the chain means either
starting again from the first request or writing my own "save progress" and retry code. With
Temporal I only described the steps, a retry policy and which errors must not be retried. When I
pointed the worker at a wrong URL, the first step was retried automatically with growing delays,
and the workflow finished as soon as I fixed the URL, without restarting it. When I killed the
worker half-way, the finished step was not repeated: a new worker continued from the saved
history. All of that retry and "remember what is done" code is code I did not have to write.

## Durability proof

Evidence from the Temporal history of the real runs (see the PR description for the full notes).

**Retry test.** Worker started with `SWAPI_BASE_URL=http://127.0.0.1:9/` (nothing listens there)
and the workflow started. While it ran: status `RUNNING`, pending activity `find_character`,
attempt 4 and counting. After restarting the worker with the correct URL (the workflow was not
restarted) it completed, and each activity was scheduled and completed once.

**Worker-crash test.** Worker started with `ACTIVITY_PAUSE_SECONDS=25`. After `find_character` had
completed and `get_homeworld` was running, the worker was killed. The workflow stayed `RUNNING`
with `find_character` completed. After starting a new worker it completed, and `find_character`
was still scheduled and completed exactly once. Note: the step that was running when the worker
died is retried only after its 30 s activity timeout expires, because Temporal cannot know the
worker is gone before that.
