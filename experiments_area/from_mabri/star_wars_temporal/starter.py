"""Starter: asks Temporal to build a dossier and prints the result.

This script does no Star Wars work itself. It only starts the workflow on
the server and waits. The worker (worker.py) has to be running somewhere,
otherwise the workflow just sits in the queue until one appears.

Run:  uv run starter.py "Luke Skywalker"
"""

import asyncio
import json
import os
import sys
import uuid

from temporalio.client import Client, WorkflowFailureError
from temporalio.exceptions import ApplicationError

from workflows import TASK_QUEUE, CharacterDossierWorkflow

TEMPORAL_ADDRESS = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
DEFAULT_NAME = "Luke Skywalker"

# Temporal's JSON converter sorts dict keys, so the dossier comes back
# alphabetical. Re-order it to match the format in the issue.
KEY_ORDER = ["name", "homeworld", "films", "species"]


def find_application_error(error: BaseException | None) -> ApplicationError | None:
    """Walk down the chain of causes to the error our activity raised.

    A failed workflow arrives as WorkflowFailureError -> ActivityError ->
    ApplicationError. Only the last one carries our "Character not found"
    message, so we look for it instead of printing the generic wrappers.
    """
    while error is not None:
        if isinstance(error, ApplicationError):
            return error
        error = error.__cause__
    return None


async def main() -> int:
    name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_NAME
    client = await Client.connect(TEMPORAL_ADDRESS)

    # A unique, readable ID per run: easy to find in the Web UI, and two runs
    # for the same name never clash.
    workflow_id = f"dossier-{name.lower().replace(' ', '-')}-{uuid.uuid4().hex[:8]}"
    print(f"Started workflow {workflow_id} (see http://localhost:8080)", file=sys.stderr)

    try:
        dossier = await client.execute_workflow(
            CharacterDossierWorkflow.run, name, id=workflow_id, task_queue=TASK_QUEUE
        )
    except WorkflowFailureError as error:
        cause = find_application_error(error)
        print(f"Error: {cause.message if cause else error}", file=sys.stderr)
        return 1

    ordered = {key: dossier[key] for key in KEY_ORDER if key in dossier}
    print(json.dumps(ordered, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
