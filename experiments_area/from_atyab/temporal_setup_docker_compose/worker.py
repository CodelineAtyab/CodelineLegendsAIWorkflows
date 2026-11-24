"""Temporal worker that hosts the Hello World Workflow.

Run it with:

    uv run python worker.py

The worker connects to the Temporal server from docker-compose
(localhost:7233) and polls the "hello-world" task queue.
"""

import asyncio
import os

from temporalio.client import Client
from temporalio.worker import Worker

from workflow import HelloWorldWorkflow

TEMPORAL_ADDRESS = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
TEMPORAL_NAMESPACE = os.environ.get("TEMPORAL_NAMESPACE", "default")
TASK_QUEUE = os.environ.get("TEMPORAL_TASK_QUEUE", "hello-world")


async def main() -> None:
    client = await Client.connect(TEMPORAL_ADDRESS, namespace=TEMPORAL_NAMESPACE)

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[HelloWorldWorkflow],
    )

    print(
        f"Worker started: address={TEMPORAL_ADDRESS} "
        f"namespace={TEMPORAL_NAMESPACE} task_queue={TASK_QUEUE}"
    )
    print("Press Ctrl+C to stop.")
    await worker.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nWorker stopped.")
