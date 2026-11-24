"""Start one Hello World Workflow execution and print its result.

Run the worker first (in another terminal):

    uv run python worker.py

Then:

    uv run python starter.py          # greets "World"
    uv run python starter.py Temporal # greets "Temporal"
"""

import asyncio
import os
import sys
import uuid

from temporalio.client import Client

from workflow import HelloWorldWorkflow

TEMPORAL_ADDRESS = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
TEMPORAL_NAMESPACE = os.environ.get("TEMPORAL_NAMESPACE", "default")
TASK_QUEUE = os.environ.get("TEMPORAL_TASK_QUEUE", "hello-world")


async def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "World"

    client = await Client.connect(TEMPORAL_ADDRESS, namespace=TEMPORAL_NAMESPACE)

    result = await client.execute_workflow(
        HelloWorldWorkflow.run,
        name,
        id=f"hello-world-{uuid.uuid4()}",
        task_queue=TASK_QUEUE,
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
