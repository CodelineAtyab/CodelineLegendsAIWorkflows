import uvicorn
from fastapi import FastAPI, Request

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
async def book_appointment(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    # Check missing fields
    for field in ["patient_name", "doctor", "date", "time"]:
        if not json_body.get(field):
            return {"error": f"Missing field: {field}"}

    doctor = json_body["doctor"]
    date = json_body["date"]
    time = json_body["time"]

    # Check if doctor is already booked
    if doctor_is_booked(doctor, date, time):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    new_appointment = {
        "id": next_appointment_id(),
        "patient_name": json_body["patient_name"],
        "doctor": doctor,
        "date": date,
        "time": time,
    }

    appointments.append(new_appointment)

    return {
        "message": "Appointment booked successfully!",
        "appointment": new_appointment,
    }


# PUT - Update an appointment
@app.put("/appointments/update")
async def update_appointment(
    appointment_id: int,
    incoming_request: Request,
) -> dict:
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    json_body = await incoming_request.json()

    # Keep old values if the user did not send new ones
    doctor = json_body.get("doctor", appointment["doctor"])
    date = json_body.get("date", appointment["date"])
    time = json_body.get("time", appointment["time"])

    # Check booking before changing anything
    if doctor_is_booked(doctor, date, time, appointment_id):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    # Change only allowed fields
    for field in ["patient_name", "doctor", "date", "time"]:
        if field in json_body:
            appointment[field] = json_body[field]

    return {
        "message": "Appointment updated successfully!",
        "appointment": appointment,
    }


# DELETE - Remove an appointment
@app.delete("/appointments/remove")
async def remove_appointment(appointment_id: int) -> dict:
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    appointments.remove(appointment)

    return {"message": f"Appointment {appointment_id} removed successfully!"}


# Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
