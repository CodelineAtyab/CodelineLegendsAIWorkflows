"""The dossier workflow: the recipe that runs the activities in order.

A workflow must be deterministic. When a worker restarts, Temporal replays the
workflow code against the saved history to work out where it stopped. So this
file makes no HTTP calls and uses no randomness; all real work happens in the
activities, whose saved results are reused during the replay.
"""

from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

# Temporal runs workflow code in a sandbox that re-imports modules for every
# run. "Passed through" tells it to reuse the normal import of activities.py
# (and httpx inside it), since the workflow only needs the function names.
with workflow.unsafe.imports_passed_through():
    from activities import find_character, get_film, get_homeworld

# The starter puts work on this queue and the worker listens on it. Both import
# it from here so the two names can never drift apart.
TASK_QUEUE = "star-wars-dossier"

# Wait 2s after the first failure, then 4s, 8s, 16s, then 30s each time.
# Ten attempts take about 3 minutes, which is enough time to fix a broken URL
# or turn the network back on without restarting the workflow.
RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=2),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=30),
    maximum_attempts=10,
)

# Longest time one attempt may run before Temporal counts it as failed.
# The HTTP timeout in activities.py (10s) is shorter, so it fires first.
ACTIVITY_TIMEOUT = timedelta(seconds=30)


# A dataclass instead of a dict: Temporal's JSON converter sorts dict keys
# alphabetically, but dataclass fields keep this order, which is the
# order of the example in the issue.
@dataclass
class Dossier:
    name: str
    homeworld: str
    films: list[str]


@workflow.defn
class DossierWorkflow:
    @workflow.run
    async def run(self, name: str) -> Dossier:
        """Build the dossier for one character name."""
        # Step 1: everything after this depends on the character's data.
        character = await workflow.execute_activity(
            find_character,
            name,
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=RETRY_POLICY,
        )

        # Step 2: the homeworld URL comes from step 1.
        homeworld = await workflow.execute_activity(
            get_homeworld,
            character["homeworld"],
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=RETRY_POLICY,
        )

        # Step 3: one activity per film URL from step 1, so Temporal saves
        # each title as soon as it arrives.
        films = []
        for film_url in character["films"]:
            title = await workflow.execute_activity(
                get_film,
                film_url,
                start_to_close_timeout=ACTIVITY_TIMEOUT,
                retry_policy=RETRY_POLICY,
            )
            films.append(title)

        return Dossier(name=character["name"], homeworld=homeworld, films=films)
