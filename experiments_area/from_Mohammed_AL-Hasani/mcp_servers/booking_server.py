from fastmcp import FastMCP

mcp = FastMCP("Clinic Booking Server")

patients: dict[int, dict] = {}
appointments: list[dict] = []


@mcp.tool
def register_patient(name: str, phone: str) -> dict:
    """Register a new patient and return the patient with a generated patient_id."""
    patient_id = len(patients) + 1
    patient = {"patient_id": patient_id, "name": name, "phone": phone}
    patients[patient_id] = patient
    return patient


@mcp.tool
def book_appointment(patient_id: int, doctor: str, date: str, time: str) -> dict:
    """Book an appointment for a patient with a doctor at a date and time.

    Returns the appointment, or an error dict if the patient does not exist
    or the doctor is already booked at that date and time.
    """
    if patient_id not in patients:
        return {"error": f"Patient {patient_id} does not exist"}
    for existing in appointments:
        if (
            existing["doctor"] == doctor
            and existing["date"] == date
            and existing["time"] == time
        ):
            return {"error": f"{doctor} is already booked on {date} at {time}"}
    appointment = {
        "appointment_id": len(appointments) + 1,
        "patient_id": patient_id,
        "doctor": doctor,
        "date": date,
        "time": time,
    }
    appointments.append(appointment)
    return appointment


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8001)
