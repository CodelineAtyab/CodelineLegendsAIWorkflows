from fastmcp import FastMCP

mcp = FastMCP("Hello MCP Server")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers and return the result"""
    return a + b


if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
