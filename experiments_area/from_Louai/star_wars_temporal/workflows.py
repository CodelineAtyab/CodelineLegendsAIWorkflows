"""The workflow: the "recipe" that chains the dependent SWAPI requests.

This file contains NO HTTP calls, NO random numbers and NO datetime.now().
It only decides *what* runs next and passes data along. That makes it
deterministic, so Temporal can replay it after a worker crash and land in
exactly the same place, skipping every step that already finished.
"""

import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

# Workflow code runs inside Temporal's sandbox, which re-imports modules on
# every run to catch non-determinism. Our activity/shared modules (and httpx)
# are safe and side-effect free at import time, so we let them pass through.
with workflow.unsafe.imports_passed_through():
    from activities import find_character, get_film, get_homeworld
    from shared import DossierInput

# A few attempts with a growing delay (1s, 2s, 4s, 8s ...). Enough to survive a
# flaky API, but finite: a permanently broken step fails instead of looping
# forever. Non-retryable errors (CharacterNotFound) skip this entirely.
RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=1),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=30),
    maximum_attempts=10,
)

# Max time for ONE attempt of an activity (the HTTP timeout is 10s, so this
# leaves room for the request itself plus JSON parsing).
ACTIVITY_TIMEOUT = timedelta(seconds=20)


@workflow.defn
class CharacterDossierWorkflow:
    @workflow.run
    async def run(self, data: DossierInput) -> dict:
        # Step 1: everything else depends on this result.
        character = await workflow.execute_activity(
            find_character,
            data.name,
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=RETRY_POLICY,
        )
        await self._demo_pause(data)

        # Step 2: uses the homeworld URL that step 1 returned.
        homeworld = await workflow.execute_activity(
            get_homeworld,
            character["homeworld"],
            start_to_close_timeout=ACTIVITY_TIMEOUT,
            retry_policy=RETRY_POLICY,
        )
        await self._demo_pause(data)

        # Step 3: one activity per film URL from step 1, run in parallel.
        # asyncio.gather is fine here - Temporal's event loop is deterministic,
        # and gather keeps the results in the same order as the input URLs.
        films = await asyncio.gather(
            *(
                workflow.execute_activity(
                    get_film,
                    url,
                    start_to_close_timeout=ACTIVITY_TIMEOUT,
                    retry_policy=RETRY_POLICY,
                )
                for url in character["films"]
            )
        )

        # Exact dossier format required by the issue.
        return {
            "name": character["name"],
            "homeworld": homeworld,
            "films": list(films),
        }

    @staticmethod
    async def _demo_pause(data: DossierInput) -> None:
        # workflow.sleep is a *durable timer* stored on the server, not
        # time.sleep: if the worker dies during the pause, the timer keeps
        # running and the workflow continues when a worker comes back.
        if data.step_delay_seconds > 0:
            await workflow.sleep(timedelta(seconds=data.step_delay_seconds))
