# The workflow is the "recipe": it decides WHICH steps run and in WHAT order.
# It does no real work itself (no HTTP, no files, no random numbers, no clock).
#
# Why so strict? Temporal saves every finished step in the workflow history.
# If the worker crashes, a new worker REPLAYS this code from the top and uses the
# saved results to skip steps that already ran. That only works if the code makes
# the same decisions every time, which is why all side effects live in activities.

from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

# Temporal runs workflow code inside a "sandbox" that re-imports modules to catch
# non-deterministic code. imports_passed_through() tells the sandbox: "use the
# normal import for these". This is the SDK's recommended way to import
# activities (and libraries like httpx they use) into a workflow file.
with workflow.unsafe.imports_passed_through():
    from activities import find_character, get_films, get_homeworld

# How Temporal retries a failed activity (network error, SWAPI 5xx, timeout):
# wait 2s, then 4s, 8s, 16s, then 30s each time (the cap), up to 8 attempts in
# total (about 2 minutes). The growing delay ("backoff") gives a struggling
# server time to recover instead of hammering it. Errors raised with
# non_retryable=True (like "Character not found") skip retries completely.
RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=2),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=30),
    maximum_attempts=8,
)

# Max time ONE attempt may run. If an attempt hangs past this, Temporal marks
# it as failed and retries it. get_films makes several requests, so we allow
# a bit more than a single 10s HTTP timeout.
ACTIVITY_TIMEOUT = timedelta(seconds=30)


@workflow.defn
class DossierWorkflow:
    @workflow.run
    async def run(self, name: str) -> dict:
        # Step 1: search for the character.
        character = await workflow.execute_activity(
            find_character,
            name,
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=RETRY_POLICY,
        )

        # Steps 2 and 3 are DEPENDENT requests: they need the URLs that step 1
        # returned, so we pass step 1's result into them.
        homeworld = await workflow.execute_activity(
            get_homeworld,
            character,
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=RETRY_POLICY,
        )
        films = await workflow.execute_activity(
            get_films,
            character,
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=RETRY_POLICY,
        )

        return {"name": character["name"], "homeworld": homeworld, "films": films}
