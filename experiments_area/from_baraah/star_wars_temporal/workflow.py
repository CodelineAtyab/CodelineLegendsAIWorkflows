
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

# Import activities without reloading their HTTP library
# inside Temporal's workflow sandbox.
with workflow.unsafe.imports_passed_through():
    from activities import find_character, get_films, get_homeworld


@workflow.defn
class StarWarsDossier:
    """Build a Star Wars character dossier using Temporal."""

    @workflow.run
    async def run(self, name: str) -> dict:
        """Execute activities and combine their results."""

        # Retry temporary failures, up to three attempts.
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=2),
            backoff_coefficient=2.0,
            maximum_attempts=3,
        )

        # Step 1: Find the character.
        character = await workflow.execute_activity(
            find_character,
            name,
            start_to_close_timeout=timedelta(seconds=20),
            retry_policy=retry_policy,
        )

        # Step 2: Get the character's home planet.
        homeworld = await workflow.execute_activity(
            get_homeworld,
            character["homeworld"],
            start_to_close_timeout=timedelta(seconds=20),
            retry_policy=retry_policy,
        )

        # Step 3: Get each movie title.
        films = []

        for film_url in character["films"]:
            title = await workflow.execute_activity(
                get_films,
                film_url,
                start_to_close_timeout=timedelta(seconds=60),
                retry_policy=retry_policy,
            )
            films.append(title)

        # Combine all results.
        return {
            "name": character["name"],
            "homeworld": homeworld,
            "films": films,
        }
