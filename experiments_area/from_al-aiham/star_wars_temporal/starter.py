"""Start a durable execution and keep the returned dossier usable as plain JSON."""

import argparse
import asyncio
import json
import sys
from uuid import uuid4

from temporalio.client import Client, WorkflowFailureError
from temporalio.service import RPCError

from workflows import TASK_QUEUE, StarWarsDossier


async def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Star Wars character dossier")
    parser.add_argument("name", nargs="?", default="Luke Skywalker")
    args = parser.parse_args()
    try:
        client = await Client.connect("localhost:7233")
        handle = await client.start_workflow(
            StarWarsDossier.run,
            args.name,
            # Unique IDs allow separate requests; randomness stays outside the workflow.
            id=f"star-wars-{uuid4()}",
            task_queue=TASK_QUEUE,
        )
        print(f"Workflow ID: {handle.id}", file=sys.stderr)
        result = await handle.result()
    except WorkflowFailureError as error:
        # Activity failures wrap the useful business error, so show the innermost cause.
        cause = error
        while getattr(cause, "cause", None) is not None:
            cause = cause.cause
        print(f"Workflow failed: {cause}", file=sys.stderr)
        return 1
    except (RPCError, OSError) as error:
        print(f"Could not connect to Temporal: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
