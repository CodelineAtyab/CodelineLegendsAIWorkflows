import uvicorn
from fastapi import FastAPI, Request

from appointments import (
    appointments,
    find_appointment,
    is_doctor_booked,
    next_id,
)

app = FastAPI()


@app.get("/appointments")
async def get_appointments(doctor: str | None = None, date: str | None = None) -> dict:
    filtered = []
    for appt in appointments:
        if doctor and appt["doctor"].lower() != doctor.lower():
            continue
        if date and appt["date"] != date:
            continue
        filtered.append(appt)
    return {"appointments": filtered, "count": len(filtered)}


@app.post("/appointments/book")
async def book_appointment(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()
    required_fields = ["patient_name", "doctor", "date", "time"]
    for field in required_fields:
        if field not in json_body:
            return {"error": f"Missing field: {field}"}

    patient_name = json_body["patient_name"]
    doctor = json_body["doctor"]
    date = json_body["date"]
    time = json_body["time"]

    if is_doctor_booked(doctor, date, time):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    new_appointment = {
        "id": next_id(),
        "patient_name": patient_name,
        "doctor": doctor,
        "date": date,
        "time": time,
    }
    appointments.append(new_appointment)
    return {"message": "Appointment booked successfully!", "appointment": new_appointment}


@app.put("/appointments/update")
async def update_appointment(appointment_id: int, incoming_request: Request) -> dict:
    appointment = find_appointment(appointment_id)
    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    update_fields = await incoming_request.json()

    # Compute new values or fallback to old ones
    doctor = update_fields.get("doctor", appointment["doctor"])
    date = update_fields.get("date", appointment["date"])
    time = update_fields.get("time", appointment["time"])

    if is_doctor_booked(doctor, date, time, ignore_id=appointment_id):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    # Update only provided fields except id
    for key in ["patient_name", "doctor", "date", "time"]:
        if key in update_fields:
            appointment[key] = update_fields[key]

    return {"message": "Appointment updated successfully!", "appointment": appointment}


@app.delete("/appointments/remove")
async def remove_appointment(appointment_id: int) -> dict:
    appointment = find_appointment(appointment_id)
    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}
    appointments.remove(appointment)
    return {"message": f"Appointment {appointment_id} removed successfully!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
