# Star Wars Dossier with Temporal

A durable Temporal workflow that builds a character dossier from dependent Star Wars API requests, running on Temporal + Postgres + Web UI in Docker Compose.

## Run it

```bash
cp .env.example .env        # then set your own password
docker compose up -d        # UI at http://localhost:8080
uv run worker.py            # terminal 1
uv run starter.py "Luke Skywalker"   # terminal 2
```

## Tool and prompts

I used **Claude Code**, one step at a time, and reviewed each step before moving on. My prompts were roughly:

1. "Plan how you will solve issue 295 in clear steps. Stop after each step so I can review the code. Don't go beyond the issue's examples and hints."
2. "Yes, step 1": create the branch and the uv project.
3. "Yes, step 2": the Docker Compose file for Temporal, Postgres and the UI.
4. "Yes, step 3" / "Yes, step 4" / "Yes, step 5": the activities, the workflow, then the worker and starter.
5. "Yes, durability tests": the retry test and the worker-crash test.

## Three things the AI got wrong or that I changed

1. **Deprecated Docker image.** Most tutorials use the `temporalio/auto-setup` image, but it is deprecated and stopped at server 1.29. I chose the supported `temporalio/server` and `admin-tools` images, with one-shot containers for the database schema and the `default` namespace.
2. **The server crashed on the first start.** The newer server image needs a dynamic config file, which the first Compose file didn't mount. It was then put in a `dynamicconfig/` folder, which the repo's `.gitignore` ignores, so it would never have been committed. The file now lives in the project root as `dynamic-config.yaml`.
3. **Wrong key order in the result.** The first workflow returned a dict, and Temporal's JSON converter sorted its keys (`films, homeworld, name`). The workflow now returns a `Dossier` dataclass, so the output matches the issue's example.

I also changed the films step: the issue's table has one `get_films` step, but the criteria say one HTTP request per activity. I chose one `get_film` call per film URL, so a failing film is retried alone.

## What Temporal saved me from

Without Temporal, I would have had to write my own retry loops with growing delays, decide which errors are worth retrying, and save each step's result somewhere so that a crash doesn't mean starting again from the first request. Temporal does all of that: it stores the result of every finished step in Postgres, retries only the step that failed, and lets a new worker continue where a killed one stopped. In my tests the broken homeworld request was retried until I fixed the code, and after killing the worker the completed steps were not run again.
