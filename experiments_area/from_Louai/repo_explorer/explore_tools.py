import asyncio
import os

from dotenv import load_dotenv
from fastmcp import Client

GITHUB_MCP_URL = "https://api.githubcopilot.com/mcp/"
REPO_OWNER = "CodelineAtyab"
REPO_NAME = "CodelineLegendsAIWorkflows"

load_dotenv()
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]


async def main():
    claint = claint(GITHUB_MCP_URL, auth=GITHUB_TOKEN)

    async with claint:
        print("Connected:", claint.is_connected())

        if __name__ == "__main__":
            asyncio.run(main())
            