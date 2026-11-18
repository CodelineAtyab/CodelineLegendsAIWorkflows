"""The starter: asks Temporal to run the workflow, waits for the result and prints it.

Usage: uv run starter.py "Luke Skywalker"   (the name is optional; this is the default)
"""

import asyncio
import json
import os
import sys
import uuid
from dataclasses import asdict

from dotenv import load_dotenv
from temporalio.client import Client, WorkflowFailureError

from workflow import TASK_QUEUE, CharacterDossierWorkflow

DEFAULT_CHARACTER = "Luke Skywalker"


def root_cause_message(error: BaseException) -> str:
    """Follow the chain of causes down to the original error.

    A failed workflow arrives wrapped (workflow error -> activity error -> our error), and
    only the innermost one carries the useful text such as "Character not found: ...".
    """
    while error.__cause__ is not None:
        error = error.__cause__
    return str(error)


async def main(character_name: str) -> None:
    load_dotenv()
    client = await Client.connect(os.getenv("TEMPORAL_ADDRESS", "localhost:7233"))
    try:
        dossier = await client.execute_workflow(
            CharacterDossierWorkflow.run,
            character_name,
            # A fresh id per run, so the same name can be started again and again.
            id=f"dossier-{uuid.uuid4()}",
            task_queue=TASK_QUEUE,
        )
    except WorkflowFailureError as error:
        sys.exit(f"Dossier failed: {root_cause_message(error)}")
    print(json.dumps(asdict(dossier), indent=2))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CHARACTER))
