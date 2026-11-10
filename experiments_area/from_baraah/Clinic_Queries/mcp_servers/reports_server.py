from fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Medical Reports MCP Server")

# Sample medical records stored in memory
medical_records = {
    1: [
        {
            "date": "2026-10-02",
            "diagnosis": "Flu",
            "notes": "Rest",
        }
    ],
    2: [
        {
            "date": "2026-10-05",
            "diagnosis": "Headache",
            "notes": "Follow up",
        }
    ],
}

# Sample outpatient department (OPD) records
opd_records = {
    1: [
        {
            "date": "2026-10-02",
            "department": "General",
        }
    ],
    2: [
        {
            "date": "2026-10-05",
            "department": "Neurology",
        }
    ],
}


@mcp.tool
def get_patient_medical_records(patient_id: int) -> list | dict:
    """Return medical records for a patient."""
    if patient_id not in medical_records:
        return {"error": "Patient not found"}

    return medical_records[patient_id]


@mcp.tool
def get_opd_records(patient_id: int) -> list | dict:
    """Return outpatient visit records for a patient."""
    if patient_id not in opd_records:
        return {"error": "Patient not found"}

    return opd_records[patient_id]


if __name__ == "__main__":
    mcp.run(transport="http", port=8003)
