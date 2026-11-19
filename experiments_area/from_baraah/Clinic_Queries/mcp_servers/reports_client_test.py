import asyncio

from fastmcp import Client


async def main():
    async with Client("http://127.0.0.1:8003/mcp") as client:
        # 1. List available tools
        tools = await client.list_tools()
        print("Tools:", [tool.name for tool in tools])

        # 2. Get medical records for patient 1
        records = await client.call_tool(
            "get_patient_medical_records",
            {"patient_id": 1},
        )
        print("Medical records:", records.data)

        # 3. Get OPD records for patient 1
        opd = await client.call_tool(
            "get_opd_records",
            {"patient_id": 1},
        )
        print("OPD records:", opd.data)

        # 4. Try an unknown patient
        invalid = await client.call_tool(
            "get_patient_medical_records",
            {"patient_id": 999},
        )
        print("Unknown patient:", invalid.data)


if __name__ == "__main__":
    asyncio.run(main())
