from typing import Annotated

import uvicorn
from fastapi import Body, FastAPI

from appointments import (
    appointments,
    doctor_is_booked,
    find_appointment,
    next_appointment_id,
)

app = FastAPI()


# GET - View all appointments or filter by doctor/date
@app.get("/appointments")
async def view_appointments(
    doctor: str | None = None,
    date: str | None = None,
) -> dict:
    results = []

    for appointment in appointments:
        if doctor is not None and appointment["doctor"].lower() != doctor.lower():
            continue

        if date is not None and appointment["date"] != date:
            continue

        results.append(appointment)

    return {
        "appointments": results,
        "count": len(results),
    }


# POST - Book a new appointment
@app.post("/appointments/book")
async def book_appointment(data: Annotated[dict, Body()]) -> dict:

    # Check missing fields
    for field in ["patient_name", "doctor", "date", "time"]:
        if data.get(field) is None:
            return {"error": f"Missing field: {field}"}

    doctor = data["doctor"]
    date = data["date"]
    time = data["time"]

    # Prevent double booking
    if doctor_is_booked(doctor, date, time):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    # Create new appointment
    new_appointment = {
        "id": next_appointment_id(),
        "patient_name": data["patient_name"],
        "doctor": doctor,
        "date": date,
        "time": time,
    }

    appointments.append(new_appointment)

    return {
        "message": "Appointment booked successfully!",
        "appointment": new_appointment,
    }


# PUT - Update an existing appointment
@app.put("/appointments/update")
async def update_appointment(
    appointment_id: int,
    data: Annotated[dict, Body()],
) -> dict:

    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    # Copy appointment so original stays unchanged if error occurs
    updated = appointment.copy()

    # Update only allowed fields
    for field in ["patient_name", "doctor", "date", "time"]:
        if field in data:
            updated[field] = data[field]

    doctor = updated["doctor"]
    date = updated["date"]
    time = updated["time"]

    # Check double booking 
    if doctor_is_booked(
        doctor,
        date,
        time,
        exclude_id=appointment_id,
    ):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    appointment.update(updated)

    return {
        "message": "Appointment updated successfully!",
        "appointment": appointment,
    }


# DELETE - Remove  appointment
@app.delete("/appointments/remove")
async def remove_appointment(appointment_id: int) -> dict:

    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    appointments.remove(appointment)

    return {"message": f"Appointment {appointment_id} removed successfully!"}


# Run 
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
