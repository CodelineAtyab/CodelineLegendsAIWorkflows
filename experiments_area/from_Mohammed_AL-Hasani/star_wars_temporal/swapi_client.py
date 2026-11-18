"""The tiny, plain-Python part: call one URL and return its JSON.

This file knows nothing about Temporal on purpose. Keeping the HTTP call in an ordinary
function makes it easy to read and to test by hand before wrapping it in an activity.
"""

import os
from typing import Any

import httpx

DEFAULT_BASE_URL = "https://swapi.dev/api/"

# A hard limit on one request. Without it a hung connection could block an activity until
# Temporal's own timeout fires, which is much later and harder to understand.
REQUEST_TIMEOUT_SECONDS = 10.0


def swapi_base_url() -> str:
    # Read at call time (not import time) so the retry test can point the worker at a
    # wrong URL and later fix it just by restarting the worker.
    return os.getenv("SWAPI_BASE_URL", DEFAULT_BASE_URL)


async def fetch_json(url: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    """Make exactly one GET request and return the parsed JSON body.

    Network problems raise httpx errors, and 4xx/5xx responses raise HTTPStatusError.
    Deciding which of those are worth retrying is the activity's job, not this function's.
    """
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS, follow_redirects=True) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
