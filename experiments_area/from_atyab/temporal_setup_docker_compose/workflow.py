"""Hello World Workflow definition."""

from temporalio import workflow


@workflow.defn
class HelloWorldWorkflow:
    """Takes a name and returns a greeting."""

    @workflow.run
    async def run(self, name: str) -> str:
        return f"Hello, {name}!"
