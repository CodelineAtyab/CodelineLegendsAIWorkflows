from fastmcp import FastMCP

mcp = FastMCP("Clinic Medical Reports Server")

medical_records: dict[int, list[dict[str, str]]] = {
    1: [{"date": "2026-10-02", "diagnosis": "Flu", "notes": "Rest"}],
    2: [{"date": "2026-10-15", "diagnosis": "Migraine", "notes": "Hydrate"}],
}

opd_records: dict[int, list[dict[str, str]]] = {
    1: [{"date": "2026-10-02", "department": "General"}],
    2: [{"date": "2026-10-15", "department": "Neurology"}],
}


@mcp.tool
def get_patient_medical_records(
    patient_id: int,
) -> list[dict[str, str]] | dict[str, str]:
    """Return a patient's diagnoses and notes, or an error for an unknown patient."""
    records = medical_records.get(patient_id)
    if records is None:
        return {"error": f"Unknown patient_id: {patient_id}"}
    return records


@mcp.tool
def get_opd_records(patient_id: int) -> list[dict[str, str]]:
    """Return the outpatient department visits for a patient."""
    return opd_records.get(patient_id, [])


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8003)
