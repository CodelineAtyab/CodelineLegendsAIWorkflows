from fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Booking MCP Server")

# Store data in memory
patients: dict[int, dict[str, int | str]] = {}
appointments: dict[int, dict[str, int | str]] = {}


@mcp.tool
def register_patient(name: str, phone: str) -> dict:
    """Register a new patient."""
    patient_id = len(patients) + 1

    patient: dict[str, int | str] = {
    "patient_id": patient_id,
    "name": name,
    "phone": phone,
  }

    patients[patient_id] = patient
    return patient


@mcp.tool
def book_appointment(
    patient_id: int,
    doctor: str,
    date: str,
    time: str,
) -> dict:
    """Book an appointment for a registered patient."""

    # Check if the patient exists
    if patient_id not in patients:
        return {"error": "Patient not found"}

    # Check if the doctor is already booked
    for existing_appointment in appointments.values():
      if (
        existing_appointment["doctor"] == doctor
        and existing_appointment["date"] == date
        and existing_appointment["time"] == time
        ):
        return {"error": "Doctor is already booked"}

    # Create a new appointment
    appointment_id = len(appointments) + 1

    appointment: dict[str, int | str] = {
        "appointment_id": appointment_id,
        "patient_id": patient_id,
        "doctor": doctor,
        "date": date,
        "time": time,
    }

    appointments[appointment_id] = appointment
    return appointment


if __name__ == "__main__":
    mcp.run(transport="http", port=8001)
