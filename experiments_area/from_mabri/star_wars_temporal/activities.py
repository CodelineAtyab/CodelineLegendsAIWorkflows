"""Activities: the steps that talk to the Star Wars API (SWAPI).

Every HTTP call in this project lives here and never in the workflow. The
reason: Temporal replays a workflow's code from its history to rebuild state
(for example after a worker crash). A network call would give a different
answer on replay, so it must happen in an activity, whose result Temporal
records once and then reuses.
"""

import httpx

SWAPI_BASE_URL = "https://swapi.dev/api"

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
        response.raise_for_status()
        return response.json()
