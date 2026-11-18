"""The workflow: the "recipe" that orders the steps and passes data between them.

Rules (because Temporal replays this code to rebuild state after a crash):
- No HTTP calls, file access, random numbers or datetime.now() in here.
  Anything non-deterministic goes in an activity.
- Waiting uses workflow.sleep (a durable timer stored by the server), not
  time.sleep / asyncio.sleep on the worker.
"""

import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

# Temporal runs workflow code in a sandbox that re-imports modules to catch
# non-deterministic code. Activities (and httpx) are only *referenced* here,
# never run here, so we pass them through the sandbox unchanged.
with workflow.unsafe.imports_passed_through():
    from activities import find_character, get_film, get_homeworld, get_species
    from shared import Dossier, DossierInput


# Retry policy for every activity: retry automatically with a growing delay
# (2s, 4s, 8s, 16s, 20s), then give up after 6 attempts (~50s in total).
# This replaces the hand-written "for attempt in range(...)" loops we would
# otherwise need. Non-retryable errors (character not found) skip it entirely.
RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=2),
    backoff_coefficient=2.0,
    maximum_interval=timedelta(seconds=20),
    maximum_attempts=6,
)

# Max time ONE attempt may take. Slightly longer than the 10s HTTP timeout in
# activities.py, so normally httpx times out first with a clearer error.
ACTIVITY_TIMEOUT = timedelta(seconds=15)


@workflow.defn
class CharacterDossierWorkflow:
    @workflow.run
    async def run(self, input: DossierInput) -> Dossier:
        # Same options for every step, so they live in one dict.
        opts = {"start_to_close_timeout": ACTIVITY_TIMEOUT, "retry_policy": RETRY_POLICY}

        # Step 1: everything else depends on this result.
        character = await workflow.execute_activity(find_character, input.name, **opts)
        await self._pause(input)

        # Step 2: uses the homeworld URL from step 1.
        homeworld = await workflow.execute_activity(get_homeworld, character["homeworld"], **opts)
        await self._pause(input)

        # Step 3: one activity per film URL from step 1, run in parallel.
        # asyncio.gather is safe in a workflow: Temporal records each activity
        # and gather keeps the results in the same order as the input list.
        films = await asyncio.gather(
            *(workflow.execute_activity(get_film, url, **opts) for url in character["films"])
        )

        # Step 4 (optional): only if asked for AND the character has a species.
        # This "if" is deterministic: it depends only on the input and on
        # step 1's recorded result, so a replay takes the same branch.
        species = None
        if input.include_species and character["species"]:
            species = await workflow.execute_activity(get_species, character["species"][0], **opts)

        # Combine everything into the dossier (exact keys from the issue).
        return Dossier(
            name=character["name"], homeworld=homeworld, films=list(films), species=species
        )

    async def _pause(self, input: DossierInput) -> None:
        """Optional durable pause between steps, only used for the crash demo."""
        if input.step_delay_seconds > 0:
            await workflow.sleep(timedelta(seconds=input.step_delay_seconds))
