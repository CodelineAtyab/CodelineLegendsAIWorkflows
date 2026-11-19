# The worker is the program that actually RUNS our workflow and activities.
# The Temporal server only stores state and hands out tasks; it never runs our
# Python code. Start this in its own terminal and leave it running.
#
# Why a separate long-running worker? If it crashes, nothing is lost: the
# server keeps the workflow history, and a restarted worker picks up exactly
# where the old one stopped.

import asyncio
from concurrent.futures import ThreadPoolExecutor

from temporalio.client import Client
from temporalio.worker import Worker

from activities import find_character, get_films, get_homeworld
from workflows import DossierWorkflow

# The worker only picks up tasks from this queue. starter.py must use the
# same name, otherwise the workflow waits forever with nobody to run it.
TASK_QUEUE = "star-wars-dossier"


async def main() -> None:
    # localhost:7233 is the Temporal port published in docker-compose.yml.
    client = await Client.connect("localhost:7233", namespace="default")

    # Our activities are normal (non-async) functions that use blocking httpx
    # calls. The SDK runs such activities in this thread pool so they don't
    # block the worker's event loop.
    with ThreadPoolExecutor(max_workers=10) as activity_executor:
        worker = Worker(
            client,
            task_queue=TASK_QUEUE,
            workflows=[DossierWorkflow],
            activities=[find_character, get_homeworld, get_films],
            activity_executor=activity_executor,
        )
        print(f"Worker started on task queue '{TASK_QUEUE}'. Press Ctrl+C to stop.")
        await worker.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Ctrl+C is the normal way to stop the worker, so no traceback.
        print("Worker stopped.")
