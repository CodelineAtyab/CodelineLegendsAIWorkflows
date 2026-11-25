import asyncio
import os

from dotenv import load_dotenv
from fastmcp import Client

GITHUB_MCP_URL = "https://api.githubcopilot.com/mcp/"
MAX_ITEMS = 5

load_dotenv()
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]


async def get_open_issues(owner, repo):
    async with Client(GITHUB_MCP_URL, auth=GITHUB_TOKEN) as client:
        await client.list_tools()
        result = await client.call_tool(
            "list_issues",
            {
                "owner": owner,
                "repo": repo,
                "state": "OPEN",
                "perPage": MAX_ITEMS,
                "fields": ["number", "title"],
            },
        )
    issues = result.structured_content["issues"]
    return [f"#{issue['number']} {issue['title']}" for issue in issues]


async def get_recent_commits(owner, repo):
    async with Client(GITHUB_MCP_URL, auth=GITHUB_TOKEN) as client:
        await client.list_tools()
        result = await client.call_tool(
            "list_commits",
            {
                "owner": owner,
                "repo": repo,
                "perPage": MAX_ITEMS,
            },
        )
    commits = result.structured_content
    return [
        f"{commit['sha'][:7]} {commit['commit']['message'].splitlines()[0]}"
        for commit in commits
    ]


if __name__ == "__main__":
    print(asyncio.run(get_open_issues("CodelineAtyab", "CodelineLegendsAIWorkflows")))
    print(asyncio.run(get_recent_commits("CodelineAtyab", "CodelineLegendsAIWorkflows")))
