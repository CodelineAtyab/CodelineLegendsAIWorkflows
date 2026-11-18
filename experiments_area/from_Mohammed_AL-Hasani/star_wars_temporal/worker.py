"""The worker: a long-running process that executes workflows and activities.

Temporal itself never runs our code. It only stores history and hands out tasks. This worker
polls the task queue, runs the code, and reports results back. If it is killed, Temporal keeps
the history, and a new worker simply continues from the last completed step.
"""

import asyncio
import os

from dotenv import load_dotenv
from temporalio.client import Client
from temporalio.worker import Worker

from activities import find_character, get_films, get_homeworld
from workflow import TASK_QUEUE, CharacterDossierWorkflow


async def main() -> None:
    load_dotenv()
    client = await Client.connect(os.getenv("TEMPORAL_ADDRESS", "localhost:7233"))
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[CharacterDossierWorkflow],
        activities=[find_character, get_homeworld, get_films],
    )
    print(f"Worker listening on task queue '{TASK_QUEUE}'. Press Ctrl+C to stop.")
    await worker.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker stopped.")
