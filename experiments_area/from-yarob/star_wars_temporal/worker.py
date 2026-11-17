"""Worker: the process that actually runs our workflow and activity code.

The Temporal server never runs our Python code. It only stores history and
hands out tasks. This worker polls the task queue, runs what it receives and
reports results back. If the worker dies, the tasks wait on the server until
a worker comes back, which is why a crash does not lose any progress.

Run:  uv run worker.py      (stop with Ctrl+C)
"""

import asyncio
import logging

from temporalio.client import Client
from temporalio.worker import Worker

from activities import find_character, get_film, get_homeworld, get_species
from shared import TASK_QUEUE, TEMPORAL_ADDRESS
from workflow import CharacterDossierWorkflow


async def main() -> None:
    # INFO level so the activity log lines (with attempt numbers) are shown.
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    client = await Client.connect(TEMPORAL_ADDRESS)

    # Register exactly the workflow and activities this worker can run.
    # A task for something not registered here would fail on this worker.
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[CharacterDossierWorkflow],
        activities=[find_character, get_homeworld, get_film, get_species],
    )
    print(f"Worker started on task queue {TASK_QUEUE!r}. Press Ctrl+C to stop.")
    # Runs until the process is stopped.
    await worker.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker stopped.")
