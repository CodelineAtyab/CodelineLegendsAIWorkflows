import uvicorn
from fastapi import FastAPI, Request

from appointments import (
    appointments,
    find_appointment,
    is_booked,
    next_id,
)

# Create FastAPI application
app = FastAPI()


# 1. GET - View all appointments or filter by doctor/date
@app.get("/appointments")
async def get_appointments(
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

    return {"appointments": results, "count": len(results)}


# 2. POST - Book a new appointment
@app.post("/appointments/book")
async def book_appointment(request: Request) -> dict:
    body = await request.json()

    # Check for missing fields
    for field in ["patient_name", "doctor", "date", "time"]:
        if not body.get(field):
            return {"error": f"Missing field: {field}"}

    # Check if doctor is already booked
    if is_booked(body["doctor"], body["date"], body["time"]):
        return {
            "error": (
                f"{body['doctor']} is already booked "
                f"on {body['date']} at {body['time']}"
            )
        }

    # Create new appointment
    new_appointment = {
        "id": next_id(),
        "patient_name": body["patient_name"],
        "doctor": body["doctor"],
        "date": body["date"],
        "time": body["time"],
    }

    # Add to the appointments list
    appointments.append(new_appointment)

    return {
        "message": "Appointment booked successfully!",
        "appointment": new_appointment,
    }


# 3. PUT - Update an existing appointment
@app.put("/appointments/update")
async def update_appointment(
    appointment_id: int,
    request: Request,
) -> dict:
    # Find appointment
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    body = await request.json()

    # Use new values if provided, otherwise keep old values
    doctor = body.get("doctor", appointment["doctor"])
    date = body.get("date", appointment["date"])
    time = body.get("time", appointment["time"])

    # Check if another appointment uses this slot
    if is_booked(doctor, date, time, appointment_id):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    # Update only the fields provided
    for field in ["patient_name", "doctor", "date", "time"]:
        if field in body:
            appointment[field] = body[field]

    return {
        "message": "Appointment updated successfully!",
        "appointment": appointment,
    }


# 4. DELETE - Remove an appointment
@app.delete("/appointments/remove")
async def remove_appointment(appointment_id: int) -> dict:
    # Find appointment
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    # Remove it from the list
    appointments.remove(appointment)

    return {"message": f"Appointment {appointment_id} removed successfully!"}


# Start the API server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
