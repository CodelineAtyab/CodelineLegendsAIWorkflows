
import asyncio

from fastmcp import Client


async def main():
    async with Client("http://127.0.0.1:8001/mcp") as client:

        # 1. List available MCP tools
        tools = await client.list_tools()
        print("Tools:", [tool.name for tool in tools])

        # 2. Register a patient
        patient = await client.call_tool(
            "register_patient",
            {
                "name": "Salim",
                "phone": "99112233",
            },
        )
        print("Patient:", patient.data)

        # 3. Book an appointment
        booking = await client.call_tool(
            "book_appointment",
            {
                "patient_id": 1,
                "doctor": "Dr. Huda",
                "date": "2026-11-20",
                "time": "10:00",
            },
        )
        print("Booking:", booking.data)

        # 4. Try booking the same slot again
        duplicate = await client.call_tool(
            "book_appointment",
            {
                "patient_id": 1,
                "doctor": "Dr. Huda",
                "date": "2026-11-20",
                "time": "10:00",
            },
        )
        print("Duplicate booking:", duplicate.data)

        # 5. Try booking with an unknown patient
        invalid = await client.call_tool(
            "book_appointment",
            {
                "patient_id": 999,
                "doctor": "Dr. Huda",
                "date": "2026-11-21",
                "time": "11:00",
            },
        )
        print("Unknown patient:", invalid.data)


if __name__ == "__main__":
    asyncio.run(main())
