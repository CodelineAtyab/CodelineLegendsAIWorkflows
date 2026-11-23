
import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from activities import find_character, get_films, get_homeworld
from workflow import StarWarsDossier


async def main():
    """Connect to Temporal and run the worker."""

    # Connect to the Temporal server running in Docker.
    client = await Client.connect("localhost:7233")

    # Register the workflow and its activities.
    worker = Worker(
        client,
        task_queue="star-wars-task-queue",
        workflows=[StarWarsDossier],
        activities=[
            find_character,
            get_homeworld,
            get_films,
        ],
    )

    # Keep the worker running to process tasks.
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
