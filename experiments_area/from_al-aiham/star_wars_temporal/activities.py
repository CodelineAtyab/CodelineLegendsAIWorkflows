"""Keep network I/O in activities so Temporal can retry it and save its results."""

import httpx
from temporalio import activity
from temporalio.exceptions import ApplicationError


async def fetch_json(url: str, params: dict | None = None) -> dict:
    # One bounded request per invocation lets Temporal own retries rather than HTTP code.
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


@activity.defn
async def find_character(name: str) -> dict:
    activity.logger.info("Searching for %s (attempt %s)", name, activity.info().attempt)
    data = await fetch_json("https://swapi.dev/api/people/", {"search": name})
    if not data["results"]:
        # A missing character is a business result; another network attempt cannot fix it.
        raise ApplicationError(
            f"Character '{name}' was not found.",
            type="CharacterNotFound",
            non_retryable=True,
        )
    return data["results"][0]


@activity.defn
async def get_homeworld(url: str) -> str:
    activity.logger.info("Fetching homeworld (attempt %s)", activity.info().attempt)
    return (await fetch_json(url))["name"]


@activity.defn
async def get_films(url: str) -> str:
    # Fetch one film per activity so a failed title does not repeat completed film requests.
    activity.logger.info("Fetching film %s (attempt %s)", url, activity.info().attempt)
    return (await fetch_json(url))["title"]
