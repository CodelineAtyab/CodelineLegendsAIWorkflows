import uvicorn
from fastapi import FastAPI, Request

from appointments import appointments, find_appointment, get_next_id, is_doctor_booked

app = FastAPI()


@app.get("/appointments")
async def get_appointments(
    doctor: str | None = None,
    date: str | None = None,
) -> dict:
    """Return all appointments matching optional doctor and date query parameters."""
    filtered = []
    for appt in appointments:
        if doctor is not None and appt["doctor"].lower() != doctor.lower():
            continue
        if date is not None and appt["date"] != date:
            continue
        filtered.append(appt)

    return {"appointments": filtered, "count": len(filtered)}


@app.post("/appointments/book")
async def book_appointment(request: Request) -> dict:
    """Book a new appointment if all fields are present and doctor slot is free."""
    body = await request.json()

    for field in ("patient_name", "doctor", "date", "time"):
        if body.get(field) is None:
            return {"error": f"Missing field: {field}"}

    doctor = body["doctor"]
    date = body["date"]
    time = body["time"]

    if is_doctor_booked(doctor, date, time):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    new_appt = {
        "id": get_next_id(),
        "patient_name": body["patient_name"],
        "doctor": doctor,
        "date": date,
        "time": time,
    }
    appointments.append(new_appt)

    return {
        "message": "Appointment booked successfully!",
        "appointment": new_appt,
    }


@app.put("/appointments/update")
async def update_appointment(
    appointment_id: int,
    request: Request,
) -> dict:
    """Update existing appointment fields without ID change or slot conflict."""
    body = await request.json()
    appt = find_appointment(appointment_id)

    if appt is None:
        return {"error": f"Appointment {appointment_id} not found"}

    draft = appt.copy()
    for field in ("patient_name", "doctor", "date", "time"):
        if field in body:
            draft[field] = body[field]

    doctor = draft["doctor"]
    date = draft["date"]
    time = draft["time"]

    if is_doctor_booked(doctor, date, time, exclude_id=appointment_id):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    appt.update(draft)
    return {
        "message": "Appointment updated successfully!",
        "appointment": appt,
    }


@app.delete("/appointments/remove")
async def remove_appointment(appointment_id: int) -> dict:
    """Delete an appointment by ID."""
    appt = find_appointment(appointment_id)

    if appt is None:
        return {"error": f"Appointment {appointment_id} not found"}

    appointments.remove(appt)
    return {"message": f"Appointment {appointment_id} removed successfully!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
