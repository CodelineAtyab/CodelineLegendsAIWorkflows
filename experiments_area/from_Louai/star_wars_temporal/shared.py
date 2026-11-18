"""Constants and data types shared by the worker, the starter and the workflow.

Keeping them in one small module means worker.py and starter.py can never
disagree about the task queue name or the shape of the workflow input.
"""

import os
from dataclasses import dataclass

# The worker polls this queue and the starter puts work on it.
# If the two names differ, the workflow just sits there "Running" forever.
TASK_QUEUE = "star-wars-dossier"

# Where the Temporal server's gRPC port is (see docker-compose.yml).
TEMPORAL_ADDRESS = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")


@dataclass
class DossierInput:
    """Workflow input. A dataclass (not loose args) so fields can be added later
    without breaking workflows that are already running."""

    name: str
    # Durable pause between steps. Only for the worker-crash demo: it gives you
    # time to kill the worker "mid-way". 0 = normal run.
    step_delay_seconds: float = 0
