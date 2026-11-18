"""The workflow: the recipe that says which steps run, in what order, and how data flows.

This file must stay deterministic (no HTTP calls, no randomness, no clock). Temporal rebuilds
the workflow's state by replaying it against the saved history, so it has to make the same
decisions every time. All real work lives in activities.py.
"""

from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

# Activities are imported "passed through" because the workflow sandbox would otherwise
# re-import (and try to restrict) httpx and friends, which the workflow never uses directly.
with workflow.unsafe.imports_passed_through():
    from activities import find_character, get_films, get_homeworld

TASK_QUEUE = "star-wars-dossier"

# Growing delay between attempts (1s, 2s, 4s, ... capped at 30s) so a flaky API gets room to
# recover instead of being hammered. Ten attempts is about two and a half minutes of trying,
# which is enough time to fix a problem by hand during the retry test.
RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=30),
    maximum_attempts=10,
)

# Upper limit for ONE attempt of an activity. A hung attempt is cancelled and retried.
ACTIVITY_TIMEOUT = timedelta(seconds=30)


@dataclass
class Dossier:
    """The workflow result. A dataclass keeps the fields in a fixed, documented order
    (Temporal's JSON encoding sorts plain dict keys alphabetically)."""

    name: str
    homeworld: str
    films: list[str]


@workflow.defn
class CharacterDossierWorkflow:
    @workflow.run
    async def run(self, character_name: str) -> Dossier:
        # Step 1 needs only the input name.
        character = await workflow.execute_activity(
            find_character,
            character_name,
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=RETRY_POLICY,
        )

        # Steps 2 and 3 are dependent: they use URLs found by step 1. Temporal stores each
        # finished result, so if the worker dies here, step 1 is not run again.
        homeworld = await workflow.execute_activity(
            get_homeworld,
            character["homeworld"],
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=RETRY_POLICY,
        )
        films = await workflow.execute_activity(
            get_films,
            character["films"],
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=RETRY_POLICY,
        )

        return Dossier(name=character["name"], homeworld=homeworld, films=films)
