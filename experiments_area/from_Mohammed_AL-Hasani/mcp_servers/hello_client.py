import asyncio

from fastmcp import Client


async def main() -> None:
    async with Client("http://127.0.0.1:8000/mcp") as client:
        result = await client.call_tool("add", {"a": 2, "b": 3})
        print(result.data)


if __name__ == "__main__":
    asyncio.run(main())
