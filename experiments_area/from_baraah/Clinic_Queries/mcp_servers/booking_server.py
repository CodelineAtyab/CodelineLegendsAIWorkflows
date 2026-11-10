
from fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Booking MCP Server")

# Store data in memory
patients = {}
appointments = {}


@mcp.tool
def register_patient(name: str, phone: str) -> dict:
    """Register a new patient."""
    patient_id = len(patients) + 1

    patient = {
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
    for appointment in appointments.values():
        if (
            appointment["doctor"] == doctor
            and appointment["date"] == date
            and appointment["time"] == time
        ):
            return {"error": "Doctor is already booked"}

    # Create a new appointment
    appointment_id = len(appointments) + 1

    appointment = {
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
