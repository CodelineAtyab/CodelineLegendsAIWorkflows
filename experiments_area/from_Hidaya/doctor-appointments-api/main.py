import uvicorn
from fastapi import Body, FastAPI

from appointments import (
    appointments,
    build_conflict_error,
    find_appointment,
    generate_next_id,
    is_doctor_booked,
)

app = FastAPI()


@app.get("/appointments")
async def view_appointments(
    doctor: str | None = None,
    date: str | None = None,
) -> dict:
    """Return appointments matching the optional filters."""
    filtered_appointments = []

    for appointment in appointments:
        if doctor is not None:
            if appointment["doctor"].lower() != doctor.lower():
                continue

        if date is not None:
            if appointment["date"] != date:
                continue

        filtered_appointments.append(appointment)

    return {
        "appointments": filtered_appointments,
        "count": len(filtered_appointments),
    }


@app.post("/appointments/book")
async def book_appointment(data: dict = Body(...)) -> dict:
    """Book an appointment if the required fields and slot are available."""
    required_fields = ("patient_name", "doctor", "date", "time")

    for field in required_fields:
        if field not in data:
            return {"error": f"Missing field: {field}"}

    if is_doctor_booked(data["doctor"], data["date"], data["time"]):
        return build_conflict_error(
            data["doctor"], data["date"], data["time"]
        )

    appointment = {
        "id": generate_next_id(),
        "patient_name": data["patient_name"],
        "doctor": data["doctor"],
        "date": data["date"],
        "time": data["time"],
    }

    appointments.append(appointment)

    return {
        "message": "Appointment booked successfully!",
        "appointment": appointment,
    }


@app.put("/appointments/update")
async def update_appointment(
    appointment_id: int,
    data: dict = Body(...),
) -> dict:
    """Update only the supplied booking fields if the slot is available."""
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    updated_appointment = appointment.copy()

    for field in ("patient_name", "doctor", "date", "time"):
        if field in data:
            updated_appointment[field] = data[field]

    if is_doctor_booked(
        updated_appointment["doctor"],
        updated_appointment["date"],
        updated_appointment["time"],
        exclude_id=appointment_id,
    ):
        return build_conflict_error(
            updated_appointment["doctor"],
            updated_appointment["date"],
            updated_appointment["time"],
        )

    appointment.update(updated_appointment)

    return {
        "message": "Appointment updated successfully!",
        "appointment": appointment,
    }


@app.delete("/appointments/remove")
async def remove_appointment(appointment_id: int) -> dict:
    """Remove an appointment by its id."""
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    appointments.remove(appointment)

    return {
        "message": f"Appointment {appointment_id} removed successfully!"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
