# Activities = the steps of our workflow that touch the outside world.
#
# Why are the HTTP calls activities and not inside the workflow?
#   A workflow must be "deterministic": when a worker restarts, Temporal replays
#   the workflow code from the start and must get the same decisions each time.
#   A network call can give a different answer (or fail) each time, so it must
#   live in an activity. Temporal records each activity's RESULT in the workflow
#   history, so on replay it reuses the saved result instead of calling SWAPI again.
#
# Why let errors simply raise?
#   If SWAPI is down, slow, or returns a 5xx error, httpx raises an exception.
#   We do NOT catch it: Temporal sees the failure and retries the activity for us
#   (following the RetryPolicy in workflows.py). No retry loops in our code.

import httpx
from temporalio import activity
from temporalio.exceptions import ApplicationError

SWAPI_BASE_URL = "https://swapi.dev/api"


def fetch_json(url: str, params: dict | None = None) -> dict:
    # timeout=10: a hanging request would otherwise block the activity forever.
    response = httpx.get(url, params=params, timeout=10)
    # Turn 4xx/5xx responses into exceptions so Temporal can retry them.
    response.raise_for_status()
    return response.json()


@activity.defn
def find_character(name: str) -> dict:
    # httpx encodes the search text for the URL (spaces etc.) via params=.
    data = fetch_json(f"{SWAPI_BASE_URL}/people/", params={"search": name})
    if not data["results"]:
        # Why non_retryable=True?
        #   Retrying cannot fix this: the character will still not exist one
        #   second later. Marking it non-retryable makes the workflow fail fast
        #   with a clear message instead of retrying (and waiting) for nothing.
        raise ApplicationError(f"Character not found: {name}", non_retryable=True)
    # SWAPI search can return several matches; we take the first one.
    return data["results"][0]


@activity.defn
def get_homeworld(character: dict) -> str:
    # This request DEPENDS on find_character: we need its "homeworld" URL first.
    planet = fetch_json(character["homeworld"])
    return planet["name"]


@activity.defn
def get_films(character: dict) -> list[str]:
    # Also depends on find_character: one request per film URL it gave us.
    titles = []
    for film_url in character["films"]:
        film = fetch_json(film_url)
        titles.append(film["title"])
    return titles
