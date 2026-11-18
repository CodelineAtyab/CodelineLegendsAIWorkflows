"""Worker: the process that actually runs workflows and activities.

The Temporal server never runs our code itself. It only stores history and
hands out tasks. This worker polls the task queue, runs whatever it receives
and reports the results back. That split is what makes the crash test work:
kill this process and the server still knows exactly which steps finished,
so a new worker simply carries on.

Run:  uv run worker.py      (stop with Ctrl+C)
"""

import asyncio
import os

from temporalio.client import Client
from temporalio.worker import Worker

from activities import find_character, get_film, get_homeworld, get_species
from workflows import TASK_QUEUE, CharacterDossierWorkflow

# localhost:7233 is the port docker-compose.yml publishes. Overridable so the
# same script works against a Temporal server somewhere else.
TEMPORAL_ADDRESS = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")


async def main() -> None:
    client = await Client.connect(TEMPORAL_ADDRESS)
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[CharacterDossierWorkflow],
        # The activities are `async def`, so they run on this event loop and
        # no thread pool (activity_executor) is needed.
        activities=[find_character, get_homeworld, get_film, get_species],
    )
    print(f"Worker listening on task queue {TASK_QUEUE!r} at {TEMPORAL_ADDRESS}. Ctrl+C to stop.")
    await worker.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Stopping mid-workflow is safe: unfinished work stays on the server
        # and resumes when a worker starts again.
        print("Worker stopped.")
