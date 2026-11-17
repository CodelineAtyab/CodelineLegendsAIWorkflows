"""Starter: asks Temporal to run one dossier workflow and prints the result.

Run: uv run starter.py "Luke Skywalker"
The worker must be running, otherwise the workflow waits on the queue.
"""

import asyncio
import json
import sys
from dataclasses import asdict

from temporalio.client import Client, WorkflowFailureError

from workflow import TASK_QUEUE, DossierWorkflow


async def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "Luke Skywalker"
    client = await Client.connect("localhost:7233")

    try:
        # Starts the workflow and waits for its result. A readable ID makes
        # the run easy to find in the UI, and Temporal refuses to start a
        # second run with the same ID while the first is still running.
        dossier = await client.execute_workflow(
            DossierWorkflow.run,
            name,
            id=f"dossier-{name.lower().replace(' ', '-')}",
            task_queue=TASK_QUEUE,
        )
    except WorkflowFailureError as error:
        # Follow the chain of causes to the original error. For an unknown
        # name: WorkflowFailureError -> ActivityError -> ApplicationError.
        reason: BaseException = error
        while reason.__cause__ is not None:
            reason = reason.__cause__
        # sys.exit with a message prints it and exits with code 1.
        sys.exit(f"Dossier failed: {reason}")

    print(json.dumps(asdict(dossier), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
