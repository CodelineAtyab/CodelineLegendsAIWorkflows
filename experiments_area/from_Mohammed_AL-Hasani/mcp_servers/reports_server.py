from fastmcp import FastMCP

mcp = FastMCP("Clinic Medical Reports Server")

medical_records: dict[int, list[dict]] = {
    1: [{"date": "2026-10-02", "diagnosis": "Flu", "notes": "Rest"}],
    2: [{"date": "2026-09-15", "diagnosis": "Asthma", "notes": "Use inhaler daily"}],
}

opd_records: dict[int, list[dict]] = {
    1: [{"date": "2026-10-02", "department": "General"}],
    2: [{"date": "2026-09-15", "department": "Respiratory"}],
}


@mcp.tool
def get_patient_medical_records(patient_id: int) -> list[dict] | dict:
    """Return a patient's medical records (date, diagnosis, notes).

    Returns an error dict if the patient is unknown.
    """
    if patient_id not in medical_records:
        return {"error": f"Patient {patient_id} not found"}
    return medical_records[patient_id]


@mcp.tool
def get_opd_records(patient_id: int) -> list[dict] | dict:
    """Return a patient's outpatient visits (date, department).

    Returns an error dict if the patient is unknown.
    """
    if patient_id not in opd_records:
        return {"error": f"Patient {patient_id} not found"}
    return opd_records[patient_id]


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8003)
