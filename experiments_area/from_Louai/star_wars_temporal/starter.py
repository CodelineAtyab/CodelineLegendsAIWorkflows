"""Starter: asks Temporal to run the dossier workflow and prints the result.

The starter does no real work itself. It only says "please run this" and waits.
Even if the starter is closed, the workflow keeps running on the server and
can be seen in the UI (http://localhost:8080).

Run:  uv run starter.py "Luke Skywalker"
      uv run starter.py "Luke Skywalker" --step-delay 15   # for the crash demo
"""

import argparse
import asyncio
import json
import re
import sys
import uuid

from temporalio.client import Client, WorkflowFailureError

from shared import TASK_QUEUE, TEMPORAL_ADDRESS, DossierInput
from workflows import CharacterDossierWorkflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a Star Wars character dossier via Temporal."
    )
    parser.add_argument(
        "name", nargs="?", default="Luke Skywalker", help="character name to search for"
    )
    parser.add_argument(
        "--step-delay",
        type=float,
        default=0,
        help="seconds to pause between steps (gives you time to kill the worker)",
    )
    return parser.parse_args()


def root_cause_message(err: BaseException) -> str:
    """Temporal wraps errors (WorkflowFailure -> ActivityError -> ApplicationError).
    Walk down to the innermost one so the user sees 'Character not found ...'."""
    while err.__cause__ is not None:
        err = err.__cause__
    return getattr(err, "message", None) or str(err)


async def main() -> int:
    args = parse_args()
    client = await Client.connect(TEMPORAL_ADDRESS)

    # Readable, unique ID so each run is easy to find in the UI.
    slug = re.sub(r"[^a-z0-9]+", "-", args.name.lower()).strip("-")
    workflow_id = f"dossier-{slug}-{uuid.uuid4().hex[:8]}"
    print(
        f"Started workflow {workflow_id} (see http://localhost:8080)", file=sys.stderr
    )

    try:
        dossier = await client.execute_workflow(
            CharacterDossierWorkflow.run,
            DossierInput(name=args.name, step_delay_seconds=args.step_delay),
            id=workflow_id,
            task_queue=TASK_QUEUE,
        )
    except WorkflowFailureError as err:
        print(f"Error: {root_cause_message(err)}", file=sys.stderr)
        return 1

    # Temporal's JSON converter sorts dict keys, so rebuild the dict in the
    # order the issue asks for (name, homeworld, films).
    ordered = {key: dossier[key] for key in ("name", "homeworld", "films")}
    print(json.dumps(ordered, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
