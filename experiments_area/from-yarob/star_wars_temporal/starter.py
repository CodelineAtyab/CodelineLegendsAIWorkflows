"""Starter: asks Temporal to run the dossier workflow and prints the result.

Usage:
    uv run starter.py                          # Luke Skywalker
    uv run starter.py "Leia Organa"
    uv run starter.py "Luke Skywalker" --step-delay 10   # for the crash test
    uv run starter.py "Chewbacca" --species              # optional step 4

The starter does not run any steps itself; it only starts the workflow and
waits. The work happens in worker.py. That means this script could even be
stopped and the workflow would still finish on the server side.
"""

import argparse
import asyncio
import json
import sys
import uuid
from dataclasses import asdict

from temporalio.client import Client, WorkflowFailureError

from shared import TASK_QUEUE, TEMPORAL_ADDRESS, DossierInput
from workflow import CharacterDossierWorkflow


def root_cause_message(err: BaseException) -> str:
    """Walk down the error chain to the original message.

    A failed activity arrives as WorkflowFailureError -> ActivityError ->
    ApplicationError("Character not found: ..."). The innermost message is
    the one a user actually needs to read.
    """
    while err.__cause__ is not None:
        err = err.__cause__
    return str(err)


async def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Star Wars character dossier.")
    parser.add_argument("name", nargs="?", default="Luke Skywalker", help="character name")
    parser.add_argument(
        "--step-delay", type=int, default=0,
        help="seconds to pause between steps (use for the worker-crash test)",
    )
    parser.add_argument(
        "--species", action="store_true",
        help="also fetch the character's species (optional stretch step 4)",
    )
    args = parser.parse_args()

    client = await Client.connect(TEMPORAL_ADDRESS)

    # A readable, unique id makes the run easy to find in the Temporal UI.
    slug = args.name.lower().replace(" ", "-")
    workflow_id = f"dossier-{slug}-{uuid.uuid4().hex[:6]}"
    print(f"Starting workflow {workflow_id} (see http://localhost:8080)", file=sys.stderr)

    try:
        dossier = await client.execute_workflow(
            CharacterDossierWorkflow.run,
            DossierInput(
                name=args.name,
                step_delay_seconds=args.step_delay,
                include_species=args.species,
            ),
            id=workflow_id,
            task_queue=TASK_QUEUE,
        )
    except WorkflowFailureError as err:
        print(f"Workflow failed: {root_cause_message(err)}", file=sys.stderr)
        return 1

    # Only the JSON goes to stdout, so the output can be piped to other tools.
    # asdict keeps the dataclass field order: name, homeworld, films.
    output = asdict(dossier)
    if not args.species:
        # Without --species, print exactly the three required keys.
        output.pop("species")
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
