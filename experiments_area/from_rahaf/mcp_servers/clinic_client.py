import asyncio

from fastmcp import Client

BOOKING_URL = "http://127.0.0.1:8001/mcp"
PHARMACY_URL = "http://127.0.0.1:8002/mcp"
REPORTS_URL = "http://127.0.0.1:8003/mcp"


async def print_tools(client: Client, server_name: str) -> None:
    """Print the tool names exposed by one connected server."""
    tools = await client.list_tools()
    print(f"{server_name} tools -> {[tool.name for tool in tools]}")


async def call_and_print(
    client: Client,
    server_name: str,
    tool_name: str,
    arguments: dict[str, object],
) -> None:
    """Call a tool and print its structured result in the required format."""
    result = await client.call_tool(tool_name, arguments)
    print(f"{server_name}.{tool_name} -> {result.data}")


async def exercise_booking_server() -> None:
    async with Client(BOOKING_URL) as client:
        await print_tools(client, "booking")
        await call_and_print(
            client,
            "booking",
            "register_patient",
            {"name": "Salim", "phone": "99112233"},
        )
        await call_and_print(
            client,
            "booking",
            "book_appointment",
            {
                "patient_id": 1,
                "doctor": "Dr. Huda",
                "date": "2026-11-20",
                "time": "10:00",
            },
        )
        await call_and_print(
            client,
            "booking",
            "book_appointment",
            {
                "patient_id": 1,
                "doctor": "Dr. Huda",
                "date": "2026-11-20",
                "time": "10:00",
            },
        )
        await call_and_print(
            client,
            "booking",
            "book_appointment",
            {
                "patient_id": 999,
                "doctor": "Dr. Huda",
                "date": "2026-11-21",
                "time": "11:00",
            },
        )


async def exercise_pharmacy_server() -> None:
    async with Client(PHARMACY_URL) as client:
        await print_tools(client, "pharmacy")
        await call_and_print(client, "pharmacy", "view_inventory", {})
        await call_and_print(
            client,
            "pharmacy",
            "add_inventory",
            {"medicine": "Amoxicillin", "quantity": 0},
        )
        await call_and_print(
            client,
            "pharmacy",
            "add_inventory",
            {"medicine": "Amoxicillin", "quantity": 30},
        )
        await call_and_print(client, "pharmacy", "view_inventory", {})


async def exercise_reports_server() -> None:
    async with Client(REPORTS_URL) as client:
        await print_tools(client, "reports")
        await call_and_print(
            client,
            "reports",
            "get_patient_medical_records",
            {"patient_id": 1},
        )
        await call_and_print(
            client,
            "reports",
            "get_opd_records",
            {"patient_id": 1},
        )
        await call_and_print(
            client,
            "reports",
            "get_patient_medical_records",
            {"patient_id": 999},
        )


async def main() -> None:
    await asyncio.gather(
        exercise_booking_server(),
        exercise_pharmacy_server(),
        exercise_reports_server(),
    )


if __name__ == "__main__":
    asyncio.run(main())
