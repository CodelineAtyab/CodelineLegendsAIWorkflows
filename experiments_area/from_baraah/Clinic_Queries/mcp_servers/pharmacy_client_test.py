
import asyncio
from fastmcp import Client


async def main():
    async with Client("http://127.0.0.1:8002/mcp") as client:

        # 1. Show available tools
        tools = await client.list_tools()
        print("Tools:", [tool.name for tool in tools])

        # 2. View existing medicines
        stock = await client.call_tool("view_inventory", {})
        print("Inventory:", stock.data)

        # 3. Add a NEW medicine
        new_medicine = await client.call_tool(
            "add_inventory",
            {
                "medicine": "Amoxicillin",
                "quantity": 30,
            },
        )
        print("New medicine:", new_medicine.data)

        # 4. Increase existing medicine stock
        updated = await client.call_tool(
            "add_inventory",
            {
                "medicine": "Paracetamol",
                "quantity": 20,
            },
        )
        print("Updated medicine:", updated.data)

        # 5. Test invalid quantity
        invalid = await client.call_tool(
            "add_inventory",
            {
                "medicine": "Ibuprofen",
                "quantity": -5,
            },
        )
        print("Invalid quantity:", invalid.data)

        # 6. View inventory again
        final_stock = await client.call_tool("view_inventory", {})
        print("Final inventory:", final_stock.data)


if __name__ == "__main__":
    asyncio.run(main())
