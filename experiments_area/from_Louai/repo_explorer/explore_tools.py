import asyncio
import os

from dotenv import load_dotenv
from fastmcp import Client

GITHUB_MCP_URL = "https://api.githubcopilot.com/mcp/"
REPO_OWNER = "CodelineAtyab"
REPO_NAME = "CodelineLegendsAIWorkflows"
MAX_ITEMS = 5

load_dotenv()
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]


async def main():
    client = Client(GITHUB_MCP_URL, auth=GITHUB_TOKEN)

    async with client:
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]
        print("tools:", tool_names)

        issues_result = await client.call_tool(
            "list_issues",
            {
                "owner": REPO_OWNER,
                "repo": REPO_NAME,
                "state": "OPEN",
                "perPage": MAX_ITEMS,
                "fields": ["number", "title"],
            },
        )
        print("list_issues ->", issues_result.structured_content)
if __name__ == "__main__":
    asyncio.run(main())


