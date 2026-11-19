"""Run Booking, Pharmacy, and Medical Reports MCP demonstrations."""

import asyncio

from fastmcp import Client

BOOKING_URL = "http://127.0.0.1:8001/mcp"
PHARMACY_URL = "http://127.0.0.1:8002/mcp"
REPORTS_URL = "http://127.0.0.1:8003/mcp"


async def run_booking() -> None:
    """Test booking tools and error cases."""
    async with Client(BOOKING_URL) as client:
        tools = await client.list_tools()
        print("Booking tools:", [tool.name for tool in tools])

        patient = await client.call_tool(
            "register_patient",
            {"name": "Salim", "phone": "99112233"},
        )
        print(f"booking.register_patient -> {patient.data}")

        patient_id = patient.data["patient_id"]
        details = {
            "patient_id": patient_id,
            "doctor": "Dr. Huda",
            "date": "2026-11-20",
            "time": "10:00",
        }

        booking = await client.call_tool("book_appointment", details)
        print(f"booking.book_appointment -> {booking.data}")

        duplicate = await client.call_tool("book_appointment", details)
        print(f"booking.book_appointment -> {duplicate.data}")

        invalid = await client.call_tool(
            "book_appointment",
            {
                "patient_id": 999,
                "doctor": "Dr. Huda",
                "date": "2026-11-21",
                "time": "11:00",
            },
        )
        print(f"booking.book_appointment -> {invalid.data}")


async def run_pharmacy() -> None:
    """Test inventory tools and invalid quantities."""
    async with Client(PHARMACY_URL) as client:
        tools = await client.list_tools()
        print("Pharmacy tools:", [tool.name for tool in tools])

        stock = await client.call_tool("view_inventory", {})
        print(f"pharmacy.view_inventory -> {stock.data}")

        updated = await client.call_tool(
            "add_inventory",
            {"medicine": "Paracetamol", "quantity": 20},
        )
        print(f"pharmacy.add_inventory -> {updated.data}")

        invalid = await client.call_tool(
            "add_inventory",
            {"medicine": "Ibuprofen", "quantity": -5},
        )
        print(f"pharmacy.add_inventory -> {invalid.data}")


async def run_reports() -> None:
    """Test medical reports and outpatient records."""
    async with Client(REPORTS_URL) as client:
        tools = await client.list_tools()
        print("Medical Reports tools:", [tool.name for tool in tools])

        records = await client.call_tool(
            "get_patient_medical_records",
            {"patient_id": 1},
        )
        print(f"reports.get_patient_medical_records -> {records.data}")

        opd = await client.call_tool(
            "get_opd_records",
            {"patient_id": 1},
        )
        print(f"reports.get_opd_records -> {opd.data}")

        invalid = await client.call_tool(
            "get_patient_medical_records",
            {"patient_id": 999},
        )
        print(f"reports.get_patient_medical_records -> {invalid.data}")


async def run_new_medicine_flow() -> None:
    """Add a new medicine and verify it appears in inventory."""
    async with Client(PHARMACY_URL) as client:
        new_medicine = await client.call_tool(
            "add_inventory",
            {"medicine": "Amoxicillin", "quantity": 30},
        )
        print(f"pharmacy.add_inventory -> {new_medicine.data}")

        inventory = await client.call_tool("view_inventory", {})
        print(f"pharmacy.view_inventory -> {inventory.data}")


async def main() -> None:
    """Run all demos, ending with the new-medicine flow."""
    await asyncio.gather(
        run_booking(),
        run_pharmacy(),
        run_reports(),
    )

    await run_new_medicine_flow()


if __name__ == "__main__":
    asyncio.run(main())
