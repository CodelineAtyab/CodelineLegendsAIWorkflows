"""Temporal activities: the steps that talk to the outside world.

Why these are activities and not code inside the workflow: a workflow must be deterministic,
because Temporal replays it from its history to recover after a crash. An HTTP call can return
something different every time, so it would break that replay. Activities are allowed to be
non-deterministic, and Temporal records their result so a completed one is never run twice.
"""

import asyncio
import os
from urllib.parse import urljoin

import httpx
from temporalio import activity
from temporalio.exceptions import ApplicationError

from swapi_client import fetch_json, swapi_base_url

# 4xx answers that are worth trying again (the server asked us to slow down / was too slow).
RETRYABLE_CLIENT_ERRORS = {408, 429}


async def pause_for_demo() -> None:
    """Optional slow-down used only to demo the worker-crash test (default: no pause).

    The real steps finish in about a second, which is too fast to kill the worker
    "mid-way". Setting ACTIVITY_PAUSE_SECONDS gives me time to do that by hand.
    """
    await asyncio.sleep(float(os.getenv("ACTIVITY_PAUSE_SECONDS", "0")))


async def get_json_or_fail_cleanly(url: str, params: dict[str, str] | None = None) -> dict:
    """Fetch JSON and decide what kind of failure a bad response is.

    - Network errors and 5xx responses are re-raised as they are: they are usually temporary,
      so Temporal's retry policy should keep trying.
    - Other 4xx responses mean our request is wrong, and asking again cannot fix that, so
      they become non-retryable errors that fail the activity immediately.
    """
    try:
        return await fetch_json(url, params)
    except httpx.HTTPStatusError as error:
        status = error.response.status_code
        if 400 <= status < 500 and status not in RETRYABLE_CLIENT_ERRORS:
            raise ApplicationError(
                f"Request to {url} was rejected with HTTP {status}",
                type="SwapiClientError",
                non_retryable=True,
            ) from error
        raise


@activity.defn
async def find_character(name: str) -> dict:
    """Step 1: search for the character and return the fields later steps depend on."""
    await pause_for_demo()
    data = await get_json_or_fail_cleanly(urljoin(swapi_base_url(), "people/"), {"search": name})
    if not data["results"]:
        # Retrying cannot make a missing character appear, so this must not be retried.
        raise ApplicationError(
            f"Character not found: {name}",
            type="CharacterNotFound",
            non_retryable=True,
        )
    first_match = data["results"][0]
    return {
        "name": first_match["name"],
        "homeworld": first_match["homeworld"],
        "films": first_match["films"],
    }


@activity.defn
async def get_homeworld(homeworld_url: str) -> str:
    """Step 2: depends on step 1, because the URL comes from the character's data."""
    await pause_for_demo()
    planet = await get_json_or_fail_cleanly(homeworld_url)
    return planet["name"]


@activity.defn
async def get_films(film_urls: list[str]) -> list[str]:
    """Step 3: depends on step 1. One request per film, sent together, titles kept in order."""
    await pause_for_demo()
    films = await asyncio.gather(*(get_json_or_fail_cleanly(url) for url in film_urls))
    return [film["title"] for film in films]
