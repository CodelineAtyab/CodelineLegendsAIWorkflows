# The starter ASKS Temporal to run a DossierWorkflow and waits for the answer.
# It does not run the workflow itself: the worker (worker.py) does that.
#
# Usage:  uv run starter.py "Luke Skywalker"

import asyncio
import json
import sys
import uuid

from temporalio.client import Client, WorkflowFailureError

from workflows import DossierWorkflow

TASK_QUEUE = "star-wars-dossier"  # must match worker.py


async def main() -> None:
    # Character name from the command line, or Luke by default.
    name = sys.argv[1] if len(sys.argv) > 1 else "Luke Skywalker"

    client = await Client.connect("localhost:7233", namespace="default")

    # Every workflow needs a unique ID. A readable name plus a short random
    # part makes it easy to find in the Web UI and lets us run Luke twice.
    # (Random values are fine HERE: this is the starter, not workflow code.)
    workflow_id = f"dossier-{name.lower().replace(' ', '-')}-{uuid.uuid4().hex[:8]}"

    try:
        dossier = await client.execute_workflow(
            DossierWorkflow.run,
            name,
            id=workflow_id,
            task_queue=TASK_QUEUE,
        )
    except WorkflowFailureError as error:
        # The real reason is wrapped in layers (workflow failed -> activity
        # failed -> ApplicationError). Walk down to the innermost cause so the
        # user sees one clean line instead of a long traceback.
        cause: BaseException = error
        while cause.__cause__ is not None:
            cause = cause.__cause__
        message = getattr(cause, "message", str(cause))
        print(f"Error: {message}")
        sys.exit(1)

    # Temporal's JSON converter sorts dict keys when it saves the result, so
    # we put them back in a reader-friendly order: name, homeworld, films.
    ordered = {key: dossier[key] for key in ("name", "homeworld", "films")}
    print(json.dumps(ordered, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
