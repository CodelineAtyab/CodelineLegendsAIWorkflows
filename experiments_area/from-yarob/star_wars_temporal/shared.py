"""Names and data types shared by the worker, the workflow and the starter.

Kept in one place because the worker and the starter MUST use the same task
queue name: if they differ, the starter puts work on a queue no worker reads,
and the workflow just sits in "Running" forever without an error.
"""

from dataclasses import dataclass

# Temporal server address (the port published by docker-compose.yml).
TEMPORAL_ADDRESS = "localhost:7233"

# The queue the worker polls and the starter sends work to.
TASK_QUEUE = "star-wars-dossier"


@dataclass
class DossierInput:
    """Workflow input.

    A dataclass (instead of plain positional arguments) lets us add fields
    later without breaking workflows that are already running.
    """

    name: str
    # Pause between steps (seconds). 0 for normal runs. Set it to e.g. 10 for
    # the worker-crash test, so there is time to kill the worker mid-way.
    # The pause is a durable Temporal timer, so it survives the crash too.
    step_delay_seconds: int = 0
    # Optional stretch step 4. Off by default so the normal output keeps the
    # exact format required by the issue (name, homeworld, films).
    include_species: bool = False


@dataclass
class Dossier:
    """Workflow result, in the exact format from the issue.

    Why a dataclass and not a plain dict: Temporal's JSON converter sorts dict
    keys, so a dict came back as films/homeworld/name. A dataclass keeps the
    field order below when the starter turns it back into JSON.
    """

    name: str
    homeworld: str
    films: list[str]
    # None when species was not requested, or when SWAPI lists no species
    # (SWAPI leaves the list empty for most humans, e.g. Luke).
    species: str | None = None
