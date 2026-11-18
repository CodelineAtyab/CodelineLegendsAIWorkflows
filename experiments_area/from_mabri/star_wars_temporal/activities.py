"""Activities: the steps that talk to the Star Wars API (SWAPI).

Every HTTP call in this project lives here and never in the workflow. The
reason: Temporal replays a workflow's code from its history to rebuild state
(for example after a worker crash). A network call would give a different
answer on replay, so it must happen in an activity, whose result Temporal
records once and then reuses.
"""

import asyncio
import os

import httpx
from temporalio import activity
from temporalio.exceptions import ApplicationError

# Both settings below exist for the durability tests in the README, so the
# tests need no code edits. Leave them unset for normal runs.
#
# SWAPI_BASE_URL: point it at a host that does not exist (for example
# https://swapi.invalid/api) to break the search step and watch Temporal
# retry it.
SWAPI_BASE_URL = os.environ.get("SWAPI_BASE_URL", "https://swapi.dev/api")

# SLOW_FILM_SECONDS: pause inside each film step, so there is time to kill
# the worker half-way through the workflow.
SLOW_FILM_SECONDS = float(os.environ.get("SLOW_FILM_SECONDS", "0"))

# SWAPI is sometimes slow. A timeout turns a "hang forever" into an error
# that Temporal's retry policy can act on.
HTTP_TIMEOUT_SECONDS = 10.0


async def fetch_json(url: str, params: dict | None = None) -> dict:
    """GET one URL and return its JSON body.

    raise_for_status() turns 4xx/5xx responses into exceptions instead of
    silently returning an error page as if it were data.
    """
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS) as client:
        response = await client.get(url, params=params)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            # Decide which failures are worth retrying. A 4xx (except 429
            # "too many requests") means the request itself is wrong, so
            # sending it again gives the same answer: fail fast. Anything
            # else (5xx, and the timeouts/connection errors httpx raises
            # before we get here) is left as a normal exception, which
            # Temporal retries according to the workflow's retry policy.
            status = error.response.status_code
            if 400 <= status < 500 and status != 429:
                raise ApplicationError(
                    f"SWAPI returned {status} for {url}",
                    type="SwapiClientError",
                    non_retryable=True,
                ) from error
            raise
        return response.json()


# --- Activities -----------------------------------------------------------
# Each one makes exactly ONE HTTP request and returns plain data (str, list,
# dict). Plain data matters because Temporal serialises every activity's
# result into the workflow history as JSON.


@activity.defn
async def find_character(name: str) -> dict:
    """Step 1: search for a character by name and keep the first match.

    Returns only the fields later steps need: the name plus the URLs that
    the next activities follow. Those URLs are what makes the requests
    dependent.
    """
    data = await fetch_json(f"{SWAPI_BASE_URL}/people/", params={"search": name})
    if not data["results"]:
        # Retrying cannot make a missing character appear, so this error is
        # non-retryable: the workflow fails at once with a clear message
        # instead of burning through every retry attempt.
        raise ApplicationError(
            f"Character not found: {name!r}",
            type="CharacterNotFound",
            non_retryable=True,
        )
    person = data["results"][0]
    return {
        "name": person["name"],
        "homeworld_url": person["homeworld"],
        "film_urls": person["films"],
        "species_urls": person["species"],
    }


@activity.defn
async def get_homeworld(url: str) -> str:
    """Step 2: follow the character's homeworld URL and return the planet name."""
    planet = await fetch_json(url)
    return planet["name"]


@activity.defn
async def get_film(url: str) -> str:
    """Step 3: fetch ONE film and return its title.

    One film per activity (instead of looping over all films here) keeps the
    issue's "one HTTP request per activity" rule. It also means Temporal
    records each title as soon as it arrives, so if the worker dies after
    film 3 of 4, only film 4 is fetched again.
    """
    if SLOW_FILM_SECONDS:
        await asyncio.sleep(SLOW_FILM_SECONDS)
    film = await fetch_json(url)
    return film["title"]


@activity.defn
async def get_species(url: str) -> str:
    """Step 4 (stretch): fetch the character's first species and return its name."""
    species = await fetch_json(url)
    return species["name"]
