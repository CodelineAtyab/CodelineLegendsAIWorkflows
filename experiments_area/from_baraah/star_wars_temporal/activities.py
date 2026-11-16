import asyncio

import httpx
from temporalio import activity
from temporalio.exceptions import ApplicationError


@activity.defn
async def find_character(name: str) -> dict:
    """Find a Star Wars character using the API."""

    url = "https://swapi.dev/api/people/"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            url,
            params={"search": name},
        )

        response.raise_for_status()
        data = response.json()

        if not data["results"]:
            raise ApplicationError(
                "Character not found",
                non_retryable=True,
            )

        return data["results"][0]


@activity.defn
async def get_homeworld(homeworld_url: str) -> str:
    """Get the character's home planet name."""

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(homeworld_url)

        response.raise_for_status()

        planet = response.json()

        return planet["name"]


@activity.defn
async def get_films(film_url: str) -> str:
    """Get a film title from the Star Wars API."""

    # Temporary delay to test worker crash recovery.
    await asyncio.sleep(20)

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(film_url)
        response.raise_for_status()

        film = response.json()
        return film["title"]

