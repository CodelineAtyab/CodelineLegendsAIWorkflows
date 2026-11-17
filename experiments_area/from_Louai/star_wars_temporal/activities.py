"""Activities: the steps that talk to the outside world (SWAPI).

Why are HTTP calls here and not in the workflow?
A workflow must be deterministic: Temporal rebuilds its state by *replaying*
the code against the stored history. An HTTP call can return something
different on every replay, so it would break that. Activities are allowed to be
non-deterministic: Temporal runs them once, records the result in history and,
on replay, just hands the recorded result back instead of calling the API again.

Rules every activity here follows:
- exactly ONE HTTP request,
- a timeout on that request (so a hanging API can't block forever),
- returns plain data (str / dict) that Temporal can serialise to JSON,
- raises a NON-retryable error when retrying cannot help (character not found,
  4xx), and lets network errors / 5xx bubble up so Temporal retries them.
"""

import os

import httpx
from temporalio import activity
from temporalio.exceptions import ApplicationError

# Configurable so the "retry test" can point the worker at a broken URL.
SWAPI_BASE_URL = os.getenv("SWAPI_BASE_URL", "https://swapi.dev/api").rstrip("/")

# Per-request timeout. Kept below the activity's start_to_close_timeout in the
# workflow, so httpx gives up first and Temporal sees a normal (retryable) error.
HTTP_TIMEOUT_SECONDS = 10.0


async def _get_json(url: str, params: dict | None = None) -> dict:
    """The tiny helper: one GET, return the JSON body.

    Error classification is the important part:
    - network error / timeout  -> httpx raises, Temporal retries (good, may be a blip)
    - 5xx or 429               -> raise_for_status raises, Temporal retries
    - other 4xx (e.g. 404)     -> non-retryable: asking again gives the same answer
    """
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS) as client:
        response = await client.get(url, params=params)

    status = response.status_code
    if 400 <= status < 500 and status not in (408, 429):
        raise ApplicationError(
            f"SWAPI returned {status} for {response.url}",
            type="ClientError",
            non_retryable=True,
        )
    response.raise_for_status()  # 5xx -> HTTPStatusError -> retried by Temporal
    return response.json()


@activity.defn
async def find_character(name: str) -> dict:
    """Step 1: search SWAPI by name and return the first match (raw person dict)."""
    activity.logger.info(
        "Searching for character %r (attempt %d)", name, activity.info().attempt
    )
    data = await _get_json(f"{SWAPI_BASE_URL}/people/", params={"search": name})

    results = data.get("results", [])
    if not results:
        # Retrying cannot create a character that does not exist, so tell
        # Temporal to stop immediately instead of burning all retry attempts.
        raise ApplicationError(
            f"Character not found: {name!r}",
            type="CharacterNotFound",
            non_retryable=True,
        )
    return results[0]


@activity.defn
async def get_homeworld(homeworld_url: str) -> str:
    """Step 2: depends on step 1 (needs the `homeworld` URL). Returns the planet name."""
    planet = await _get_json(homeworld_url)
    return planet["name"]


@activity.defn
async def get_film(film_url: str) -> str:
    """Step 3 (one call per film URL from step 1). Returns the film title.

    One activity per film instead of one activity looping over all films:
    if film 4 fails, Temporal retries only film 4 - films 1-3 are already
    saved in history and are not fetched again.
    """
    film = await _get_json(film_url)
    return film["title"]
