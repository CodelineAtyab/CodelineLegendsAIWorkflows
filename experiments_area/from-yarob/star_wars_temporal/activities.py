"""Activities: the steps that do real work (HTTP requests to SWAPI).

Why are HTTP calls here and not in the workflow?
Temporal rebuilds a workflow's state by *replaying* its code against the saved
history (for example after the worker crashes). Replay only works if the
workflow code gives the same result every time. An HTTP call does not: the API
can be slow, down, or return different data. So all I/O lives in activities.
Temporal records each activity's result in the history; on replay it reuses
the recorded result instead of calling the API again.

Each activity makes exactly ONE request, so a failure only retries that one
request, and every success is saved on its own.
"""

import os

import httpx
from temporalio import activity
from temporalio.exceptions import ApplicationError


# Read at call time (not import time) so the retry test can change it by
# restarting only the worker. Default is the real public API.
def _base_url() -> str:
    return os.environ.get("SWAPI_BASE_URL", "https://swapi.dev/api").rstrip("/")


# Timeout for a single HTTP request. Without it, a hanging connection could
# block the activity until Temporal's own (longer) timeout kills it.
HTTP_TIMEOUT_SECONDS = 10.0


async def fetch_json(url: str, params: dict | None = None) -> dict:
    """GET one URL and return the JSON body as a dict.

    Error handling decides what Temporal will retry:
    - Network errors / timeouts: we let httpx raise them. Any normal exception
      counts as *retryable* for Temporal, which is what we want: a blip may be
      gone on the next attempt.
    - 5xx and 429 (rate limit): server-side or temporary -> retryable.
    - Other 4xx (e.g. 404): the request itself is wrong; asking again gives
      the same answer -> non-retryable, fail fast.
    """
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS, follow_redirects=True) as client:
        response = await client.get(url, params=params)

    status = response.status_code
    if status >= 500 or status == 429:
        # Plain exception -> Temporal retries according to the retry policy.
        raise RuntimeError(f"SWAPI temporary error {status} for {url}")
    if status >= 400:
        raise ApplicationError(
            f"SWAPI returned {status} for {url}",
            type="BadRequest",
            non_retryable=True,
        )
    return response.json()


@activity.defn
async def find_character(name: str) -> dict:
    """Step 1: search for the character and return the first match.

    Returns plain data (a dict) so Temporal can serialise it into the history.
    """
    # activity.logger adds workflow/activity ids and the attempt number to
    # every line, so retries are visible in the worker terminal.
    activity.logger.info("Searching for %r (attempt %d)", name, activity.info().attempt)
    data = await fetch_json(f"{_base_url()}/people/", params={"search": name})

    results = data.get("results", [])
    if not results:
        # A missing character will still be missing on attempt 2, 3, 4...
        # non_retryable=True tells Temporal to fail immediately instead of
        # retrying until the policy gives up.
        raise ApplicationError(
            f"Character not found: {name!r}",
            type="CharacterNotFound",
            non_retryable=True,
        )

    character = results[0]
    # Only keep the fields later steps need. Smaller payloads = smaller history.
    return {
        "name": character["name"],
        "homeworld": character["homeworld"],
        "films": character["films"],
        "species": character.get("species", []),
    }


@activity.defn
async def get_homeworld(homeworld_url: str) -> str:
    """Step 2: depends on step 1 (the URL comes from the character)."""
    activity.logger.info("Fetching homeworld %s", homeworld_url)
    planet = await fetch_json(homeworld_url)
    return planet["name"]


@activity.defn
async def get_film(film_url: str) -> str:
    """Step 3 (called once per film URL): return the film title.

    One activity per film instead of one activity for all films: if film 3
    fails, films 1 and 2 are already saved and are not fetched again.
    """
    activity.logger.info("Fetching film %s", film_url)
    film = await fetch_json(film_url)
    return film["title"]


@activity.defn
async def get_species(species_url: str) -> str:
    """Step 4 (optional stretch): the name of the character's first species."""
    activity.logger.info("Fetching species %s", species_url)
    species = await fetch_json(species_url)
    return species["name"]
