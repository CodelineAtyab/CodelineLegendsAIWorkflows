from fastmcp import FastMCP

mcp = FastMCP("Hello Server")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two integers and return the sum."""
    return a + b


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
