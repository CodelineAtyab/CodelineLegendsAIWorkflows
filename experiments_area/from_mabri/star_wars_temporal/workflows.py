"""The workflow: the "recipe" that runs the activities in order.

A workflow must be DETERMINISTIC. When a worker restarts, Temporal re-runs
this code from the top and feeds it the recorded result of every activity
that already finished, so that the code reaches the same point again
without redoing that work ("replay"). That only works if the code takes the
same path every time, so there are no HTTP calls, no random numbers and no
reading the clock here. All of those belong in activities.
"""

from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

# The workflow file is loaded inside Temporal's sandbox, which re-imports
# modules to catch non-deterministic code. "pass through" means: import
# activities normally instead. It is safe because we only use the activity
# function references here, we never call fetch_json from the workflow.
with workflow.unsafe.imports_passed_through():
    from activities import find_character, get_film, get_homeworld, get_species

# How Temporal retries a failed activity: wait 1s, then 2s, 4s, 8s (doubling,
# capped at 30s), and give up after 5 attempts. This replaces the manual
# retry loops we would otherwise write. Errors raised as non_retryable
# (like CharacterNotFound) skip the retries entirely.
RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=30),
    maximum_attempts=5,
)

# The queue the worker listens on and the starter sends work to. Defined once
# here so the two scripts cannot drift apart: a typo in either name would
# leave the workflow waiting forever with no worker to pick it up.
TASK_QUEUE = "star-wars-dossier"

# Upper bound for ONE attempt of an activity. A little above the 10s HTTP
# timeout in activities.py, so httpx's own timeout normally fires first and
# produces a clearer error message.
ACTIVITY_TIMEOUT = timedelta(seconds=15)


@workflow.defn
class CharacterDossierWorkflow:
    @workflow.run
    async def run(self, name: str) -> dict:
        # Shared options for every activity call below.
        options = {
            "start_to_close_timeout": ACTIVITY_TIMEOUT,
            "retry_policy": RETRY_POLICY,
        }

        # Step 1: everything else depends on this result.
        character = await workflow.execute_activity(find_character, name, **options)

        # Step 2: follow the homeworld URL from step 1.
        homeworld = await workflow.execute_activity(
            get_homeworld, character["homeworld_url"], **options
        )

        # Step 3: one activity per film, one after another. Each finished
        # title is saved in the history, so a crash mid-way only repeats the
        # film that was in progress.
        films = []
        for film_url in character["film_urls"]:
            films.append(await workflow.execute_activity(get_film, film_url, **options))

        dossier = {
            "name": character["name"],
            "homeworld": homeworld,
            "films": films,
        }

        # Step 4 (stretch): SWAPI leaves `species` empty for humans like Luke,
        # so only fetch it when there is one. The key is added only then, so
        # the dossier for a human keeps the exact format from the issue.
        if character["species_urls"]:
            dossier["species"] = await workflow.execute_activity(
                get_species, character["species_urls"][0], **options
            )

        return dossier
