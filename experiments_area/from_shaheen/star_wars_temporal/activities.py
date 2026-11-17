"""Activities: the steps of the dossier workflow that talk to the Star Wars API.

The HTTP calls live here and not in the workflow because their result can be
different every time (slow API, network error). Temporal saves the result of
every finished activity, so a request that already succeeded is never sent
again, even if the worker crashes later.
"""

from typing import Any

import httpx
from temporalio import activity
from temporalio.exceptions import ApplicationError

SWAPI_BASE_URL = "https://swapi.dev/api"

# Without a timeout a stuck request could hang forever. With one, it fails,
# and Temporal retries it.
HTTP_TIMEOUT_SECONDS = 10


def fetch_json(url: str, params: dict[str, str] | None = None) -> Any:
    """Send one GET request and return the JSON body."""
    response = httpx.get(url, params=params, timeout=HTTP_TIMEOUT_SECONDS)
    # Turns 4xx and 5xx answers into an exception. We don't catch it, because
    # an exception that leaves an activity is what tells Temporal to retry.
    response.raise_for_status()
    return response.json()


@activity.defn
def find_character(name: str) -> dict[str, Any]:
    """Step 1: search for the character and keep the first match."""
    data = fetch_json(f"{SWAPI_BASE_URL}/people/", params={"search": name})
    if not data["results"]:
        # Retrying cannot make a missing character appear, so mark the error
        # as non-retryable and let the workflow fail straight away.
        raise ApplicationError(
            f"Character not found: {name}",
            type="CharacterNotFound",
            non_retryable=True,
        )
    character = data["results"][0]
    # Keep only what the next steps need. Whatever an activity returns is
    # stored in the workflow history, so smaller is better.
    return {
        "name": character["name"],
        "homeworld": character["homeworld"],
        "films": character["films"],
    }


@activity.defn
def get_homeworld(homeworld_url: str) -> str:
    """Step 2: fetch the character's homeworld and return its name."""
    planet = fetch_json(homeworld_url)
    return planet["name"]


@activity.defn
def get_film(film_url: str) -> str:
    """Step 3: fetch one film and return its title.

    The workflow calls this once per film URL. One request per activity means
    a failed film is retried alone, without fetching the other films again.
    """
    film = fetch_json(film_url)
    return film["title"]
