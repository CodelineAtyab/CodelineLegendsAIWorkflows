"""Worker: the process that actually runs the workflow and activity code.

The Temporal server never runs our Python code. It stores the history and puts
tasks on a queue; this worker picks them up, runs them and reports the results.
If the worker dies, the tasks wait on the queue until a worker is back.

Run: uv run worker.py   (stop with Ctrl+C)
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor

from temporalio.client import Client
from temporalio.worker import Worker

from activities import find_character, get_film, get_homeworld
from workflow import TASK_QUEUE, DossierWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")

    # The activities are normal blocking functions (httpx.get waits for the
    # answer), so they run in threads and don't block the worker meanwhile.
    with ThreadPoolExecutor(max_workers=10) as executor:
        worker = Worker(
            client,
            task_queue=TASK_QUEUE,
            workflows=[DossierWorkflow],
            activities=[find_character, get_homeworld, get_film],
            activity_executor=executor,
        )
        print(f"Worker listening on task queue '{TASK_QUEUE}'. Press Ctrl+C to stop.")
        await worker.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker stopped.")
