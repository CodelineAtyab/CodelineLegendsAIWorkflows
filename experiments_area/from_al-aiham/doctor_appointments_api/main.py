import uvicorn
from fastapi import FastAPI, Request

from appointments import appointments, find_appointment, get_next_id, is_doctor_booked

app = FastAPI()


@app.get("/appointments")
async def view_appointments(
    doctor: str | None = None,
    date: str | None = None,
) -> dict:
    """Return appointments matching the optional doctor and date filters."""
    result = []

    for appointment in appointments:
        if doctor is not None and appointment["doctor"].lower() != doctor.lower():
            continue

        if date is not None and appointment["date"] != date:
            continue

        result.append(appointment)

    return {"appointments": result, "count": len(result)}


@app.post("/appointments/book")
async def book_appointment(incoming_request: Request) -> dict:
    """Book an appointment when all fields are supplied and the slot is free."""
    json_body = await incoming_request.json()

    for field in ("patient_name", "doctor", "date", "time"):
        if json_body.get(field) is None:
            return {"error": f"Missing field: {field}"}

    doctor = json_body["doctor"]
    date = json_body["date"]
    time = json_body["time"]

    if is_doctor_booked(doctor, date, time):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    appointment = {
        "id": get_next_id(),
        "patient_name": json_body["patient_name"],
        "doctor": doctor,
        "date": date,
        "time": time,
    }

    appointments.append(appointment)

    return {
        "message": "Appointment booked successfully!",
        "appointment": appointment,
    }


@app.put("/appointments/update")
async def update_appointment(
    appointment_id: int,
    incoming_request: Request,
) -> dict:
    """Update supplied fields only when the resulting booking does not conflict."""
    json_body = await incoming_request.json()
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    # Check a copy first so a rejected update leaves the original unchanged.
    updated_appointment = appointment.copy()

    for field in ("patient_name", "doctor", "date", "time"):
        if field in json_body:
            updated_appointment[field] = json_body[field]

    doctor = updated_appointment["doctor"]
    date = updated_appointment["date"]
    time = updated_appointment["time"]

    if is_doctor_booked(doctor, date, time, exclude_id=appointment_id):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    appointment.update(updated_appointment)

    return {
        "message": "Appointment updated successfully!",
        "appointment": appointment,
    }


@app.delete("/appointments/remove")
async def remove_appointment(appointment_id: int) -> dict:
    """Remove an existing appointment and return a confirmation message."""
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    appointments.remove(appointment)

    return {"message": f"Appointment {appointment_id} removed successfully!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
