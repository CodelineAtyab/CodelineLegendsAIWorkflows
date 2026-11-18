from fastmcp import FastMCP

mcp = FastMCP("Clinic Booking Server")

patients: list[dict[str, int | str]] = []
appointments: list[dict[str, int | str]] = []


@mcp.tool
def register_patient(name: str, phone: str) -> dict[str, int | str]:
    """Register a patient and return their generated ID and contact details."""
    patient = {
        "patient_id": len(patients) + 1,
        "name": name,
        "phone": phone,
    }
    patients.append(patient)
    return patient


@mcp.tool
def book_appointment(
    patient_id: int, doctor: str, date: str, time: str
) -> dict[str, int | str]:
    """Book a patient with a doctor unless the patient or time slot is unavailable."""
    if not any(patient["patient_id"] == patient_id for patient in patients):
        return {"error": f"Patient {patient_id} does not exist"}

    doctor_is_booked = any(
        appointment["doctor"] == doctor
        and appointment["date"] == date
        and appointment["time"] == time
        for appointment in appointments
    )
    if doctor_is_booked:
        return {"error": f"{doctor} is already booked at {date} {time}"}

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
