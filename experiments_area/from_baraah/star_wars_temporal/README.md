# Star Wars Dossier — Temporal Workflow

## 1. Project Overview

This project uses Python, Temporal, Docker Compose, and the Star Wars API (SWAPI) to retrieve information about a Star Wars character.

The goal is to understand how Temporal manages workflows, retries failed activities, and remembers completed steps when a worker stops.

## 2. Technologies Used

- **Python:** Builds the application.
- **Temporal:** Manages the workflow, activities, and retries.
- **Docker Compose:** Runs the required containers.
- **PostgreSQL:** Stores Temporal workflow history.
- **HTTPX:** Sends requests to the Star Wars API.
- **uv:** Manages the Python project and dependencies.

## 3. How the Application Works

The workflow performs three main steps:

1. `find_character` — Searches for a Star Wars character.
2. `get_homeworld` — Retrieves the character's home planet.
3. `get_films` — Retrieves each film title.

The workflow combines the results into a JSON dossier.

Example output:

```json
{
  "name": "Luke Skywalker",
  "homeworld": "Tatooine",
  "films": [
    "A New Hope",
    "The Empire Strikes Back",
    "Return of the Jedi",
    "Revenge of the Sith"
  ]
}
```

## 4. Running the Project

Start the containers:

```bash
docker compose up -d
```

Start the Temporal Worker in the first terminal:

```bash
uv run worker.py
```

Start the workflow in a second terminal:

```bash
uv run starter.py "Luke Skywalker"
```

Open the Temporal Web UI:

http://localhost:8080

## 5. AI-Driven Development

I used ChatGPT to guide me through building the project step by step, explain the code, and help troubleshoot errors.

Example prompts:

- "Explain what Temporal is and how it works."
- "Guide me step by step through creating a Temporal workflow."
- "Explain how to create a Temporal Worker."
- "How can I test automatic retries?"
- "How can I test worker-crash recovery?"

I reviewed the suggested code and tested the application locally to understand how the components work together.

## 6. Three Corrections and Improvements

### Improvement 1 — Error Handling

I changed the character-not-found error to a non-retryable `ApplicationError`.

This prevents Temporal from repeatedly searching for a character that does not exist.

### Improvement 2 — Retry Policy

I configured a retry policy with an initial interval of 2 seconds and a maximum of 3 attempts.

This allows Temporal to retry activities when temporary errors occur.

### Improvement 3 — Activity Timeout

I increased the film activity timeout to 60 seconds during the worker-crash test.

This allowed the activity to finish despite the temporary delay used for testing.

## 7. Automatic Retry Test

I temporarily changed the `get_homeworld` URL to an invalid address.

The activity failed with:

`All connection attempts failed`

Temporal automatically retried the activity.

I verified **Attempt 3** in the Temporal Web UI.

After reaching the retry limit, the workflow failed. I restored the correct URL and successfully ran a new workflow.

## 8. Worker-Crash Recovery Test

I added a temporary delay to the `get_films` activity.

I started the workflow, stopped the Python Worker, and restarted it.

The workflow later completed successfully, returning the character's name, homeworld, and film titles.

The Temporal Web UI showed the workflow status as **Completed**.

## 9. What Temporal Saved Me From

Temporal helped me avoid writing manual retry and workflow progress-tracking logic. It keeps a history of completed activities and can continue processing after a worker interruption. Without Temporal, I would need to handle retries, store intermediate results, and implement recovery logic myself.

## 10. Conclusion

This project helped me understand how workflows and activities work together.

I also learned how to connect Python applications to Temporal, test API failures, and use the Temporal Web UI to inspect workflow execution.

### Successful Automatic Retry Recovery Test

I temporarily changed the `get_homeworld` API URL to an invalid address and configured unlimited retries for the test.

Temporal automatically retried the failed activity while keeping the workflow running.

I then stopped the Worker, restored the correct URL, and restarted the Worker without starting a new workflow.

The same workflow successfully completed.

**Workflow ID:** `star-wars-a71476dd-bd8d-489f-af70-6e817a10e76f`

**Result:** Temporal successfully recovered from a temporary API failure without restarting the workflow.