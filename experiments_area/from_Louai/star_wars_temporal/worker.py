"""Worker: the process that actually executes our workflow and activity code.

The Temporal server never runs our Python itself. It only stores history and
hands out tasks. This worker polls the task queue, runs whatever it gets, and
reports the result back. Kill it and the work simply waits on the server until
a worker comes back - nothing is lost.

Run:  uv run worker.py      (Ctrl+C to stop)
"""

import asyncio
import logging

from temporalio.client import Client
from temporalio.worker import Worker

from activities import find_character, get_film, get_homeworld
from shared import TASK_QUEUE, TEMPORAL_ADDRESS
from workflows import CharacterDossierWorkflow


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )

    client = await Client.connect(TEMPORAL_ADDRESS)
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[CharacterDossierWorkflow],
        activities=[find_character, get_homeworld, get_film],
    )
    print(
        f"Worker listening on task queue {TASK_QUEUE!r} at {TEMPORAL_ADDRESS} (Ctrl+C to stop)"
    )
    await worker.run()  # runs until the process is stopped


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker stopped.")
