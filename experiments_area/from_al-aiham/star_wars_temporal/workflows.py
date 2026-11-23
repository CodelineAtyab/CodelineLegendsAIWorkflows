"""Describe the dependent steps without performing network I/O during replay."""

from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    # These imports identify activities; HTTP runs in the worker's activity context.
    from activities import find_character, get_films, get_homeworld


TASK_QUEUE = "star-wars-dossier"


@workflow.defn
class StarWarsDossier:
    @workflow.run
    async def run(self, name: str) -> dict:
        # Bound transient failures while giving a restarted worker time to resume work.
        options = {
            "start_to_close_timeout": timedelta(seconds=20),
            "retry_policy": RetryPolicy(
                initial_interval=timedelta(seconds=2),
                backoff_coefficient=2,
                maximum_interval=timedelta(seconds=16),
                maximum_attempts=5,
            ),
        }
        character = await workflow.execute_activity(find_character, name, **options)
        homeworld = await workflow.execute_activity(
            get_homeworld, character["homeworld"], **options
        )
        films = []
        for url in character["films"]:
            # Await in order to preserve the API's film order and each saved result.
            films.append(await workflow.execute_activity(get_films, url, **options))
        return {"name": character["name"], "homeworld": homeworld, "films": films}
