"""Connect Python (LangChain/LangGraph) to the Playwright MCP server.

Two transports are supported, chosen with the PLAYWRIGHT_MCP_MODE env var:

* ``stdio`` (default): Python spawns its own ``npx @playwright/mcp`` process.
* ``http``: connect to an already running server, e.g. one started with
  ``npx @playwright/mcp@0.0.85 --port 8931``. Claude Code can connect to the
  very same server, so both agents share one browser.
"""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

PLAYWRIGHT_MCP_PACKAGE = "@playwright/mcp@0.0.85"
SERVER_NAME = "playwright"


def server_config(headless: bool = False) -> dict[str, Any]:
    """Build the MCP connection config for the selected transport."""
    mode = os.getenv("PLAYWRIGHT_MCP_MODE", "stdio").lower()
    if mode == "http":
        url = os.getenv("PLAYWRIGHT_MCP_URL", "http://localhost:8931/mcp")
        return {"transport": "streamable_http", "url": url}

    args = [
        PLAYWRIGHT_MCP_PACKAGE,
        # In-memory profile: avoids "Browser is already in use" when another
        # client (e.g. Claude Code) is running Playwright MCP at the same time.
        "--isolated",
        "--viewport-size",
        "1280x800",
    ]
    if headless:
        args.append("--headless")
    # On Windows, npx is a .cmd script, so it has to be launched through cmd.
    if os.name == "nt":
        return {
            "transport": "stdio",
            "command": "cmd",
            "args": ["/c", "npx", "-y", *args],
        }
    return {"transport": "stdio", "command": "npx", "args": ["-y", *args]}


@asynccontextmanager
async def playwright_tools(
    headless: bool = False,
) -> AsyncIterator[dict[str, BaseTool]]:
    """Yield the Playwright MCP tools, keyed by name, inside ONE session.

    Keeping a single session open matters: ``client.get_tools()`` would open a
    new MCP session (and therefore a new browser) for every tool call, so the
    page you navigated to would be gone before you could click on it.
    """
    client = MultiServerMCPClient({SERVER_NAME: server_config(headless)})  # type: ignore[dict-item]
    async with client.session(SERVER_NAME) as session:
        tools = await load_mcp_tools(session)
        yield {tool.name: tool for tool in tools}


def tool_text(result: Any) -> str:
    """Flatten an MCP tool result (str or list of content blocks) into text."""
    if isinstance(result, str):
        return result
    if isinstance(result, list):
        return "\n".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in result
        )
    return str(result)
