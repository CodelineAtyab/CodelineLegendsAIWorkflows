"""Run the process Temporal can replace without losing completed activity results."""

import asyncio
import logging

from temporalio.client import Client
from temporalio.worker import Worker

from activities import find_character, get_films, get_homeworld
from workflows import TASK_QUEUE, StarWarsDossier


async def main() -> None:
    # Poll the local Compose server so workflow history stays in its Postgres database.
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[StarWarsDossier],
        activities=[find_character, get_homeworld, get_films],
    )
    logging.info("Worker listening on task queue %s", TASK_QUEUE)
    await worker.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
