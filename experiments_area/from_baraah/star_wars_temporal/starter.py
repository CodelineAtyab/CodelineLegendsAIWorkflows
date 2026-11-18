
import asyncio
import json
import sys
from uuid import uuid4

from temporalio.client import Client, WorkflowFailureError

from workflow import StarWarsDossier


async def main():
    """Start the Star Wars workflow."""

    name = " ".join(sys.argv[1:]) or "Luke Skywalker"

    # Connect to Temporal.
    client = await Client.connect("localhost:7233")

    try:
        # Start the workflow.
        result = await client.execute_workflow(
            StarWarsDossier.run,
            name,
            id=f"star-wars-{uuid4()}",
            task_queue="star-wars-task-queue",
        )

        # Print the successful result.
        print(json.dumps(result, indent=2))

    except WorkflowFailureError as error:
        # Show a simple message instead of a long traceback.
        print(f"Workflow failed: {error.cause}")


if __name__ == "__main__":
    asyncio.run(main())
