import asyncio

from fastmcp import Client

BOOKING_URL = "http://127.0.0.1:8001/mcp"
PHARMACY_URL = "http://127.0.0.1:8002/mcp"
REPORTS_URL = "http://127.0.0.1:8003/mcp"


async def call(client: Client, server: str, tool: str, arguments: dict) -> None:
    result = await client.call_tool(tool, arguments)
    print(f"{server}.{tool} -> {result.data}")


async def list_tools(client: Client, server: str) -> None:
    tools = await client.list_tools()
    print(f"{server} tools: {[tool.name for tool in tools]}")


async def run_booking() -> None:
    async with Client(BOOKING_URL) as client:
        await list_tools(client, "booking")
        await call(client, "booking", "register_patient", {"name": "Salim", "phone": "99112233"})
        await call(
            client,
            "booking",
            "book_appointment",
            {"patient_id": 1, "doctor": "Dr. Huda", "date": "2026-11-20", "time": "10:00"},
        )
        await call(
            client,
            "booking",
            "book_appointment",
            {"patient_id": 1, "doctor": "Dr. Huda", "date": "2026-11-20", "time": "10:00"},
        )
        await call(
            client,
            "booking",
            "book_appointment",
            {"patient_id": 99, "doctor": "Dr. Huda", "date": "2026-11-21", "time": "09:00"},
        )


async def run_reports() -> None:
    async with Client(REPORTS_URL) as client:
        await list_tools(client, "reports")
        await call(client, "reports", "get_patient_medical_records", {"patient_id": 1})
        await call(client, "reports", "get_opd_records", {"patient_id": 1})
        await call(client, "reports", "get_patient_medical_records", {"patient_id": 99})


async def run_pharmacy() -> None:
    async with Client(PHARMACY_URL) as client:
        await list_tools(client, "pharmacy")
        await call(client, "pharmacy", "view_inventory", {})
        await call(client, "pharmacy", "add_inventory", {"medicine": "Ibuprofen", "quantity": 0})
        await call(client, "pharmacy", "add_inventory", {"medicine": "Amoxicillin", "quantity": 30})
        await call(client, "pharmacy", "view_inventory", {})


async def main() -> None:
    await asyncio.gather(run_booking(), run_reports())
    await run_pharmacy()


if __name__ == "__main__":
    asyncio.run(main())
