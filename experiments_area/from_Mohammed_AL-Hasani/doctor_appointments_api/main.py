import uvicorn
from fastapi import FastAPI, Request

from appointments import (
    appointments,
    create_next_id,
    find_appointment,
    is_doctor_booked,
)

app = FastAPI()


@app.get("/appointments")
async def get_appointments(
    doctor: str | None = None,
    date: str | None = None,
) -> dict:
    filtered_appointments = []

    for appointment in appointments:
        if doctor is not None and appointment["doctor"].lower() != doctor.lower():
            continue

        if date is not None and appointment["date"] != date:
            continue

        filtered_appointments.append(appointment)

    return {
        "appointments": filtered_appointments,
        "count": len(filtered_appointments),
    }


@app.post("/appointments/book")
async def book_appointment(request: Request) -> dict:
    json_body = await request.json()

    required_fields = ["patient_name", "doctor", "date", "time"]

    for field in required_fields:
        if not json_body.get(field):
            return {"error": f"Missing field: {field}"}

    patient_name = json_body["patient_name"]
    doctor = json_body["doctor"]
    date = json_body["date"]
    time = json_body["time"]

    if is_doctor_booked(doctor, date, time):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    new_appointment = {
        "id": create_next_id(),
        "patient_name": patient_name,
        "doctor": doctor,
        "date": date,
        "time": time,
    }

    appointments.append(new_appointment)

    return {
        "message": "Appointment booked successfully!",
        "appointment": new_appointment,
    }


@app.put("/appointments/update")
async def update_appointment(
    appointment_id: int,
    request: Request,
) -> dict:
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    json_body = await request.json()

    new_doctor = json_body.get("doctor", appointment["doctor"])
    new_date = json_body.get("date", appointment["date"])
    new_time = json_body.get("time", appointment["time"])

    if is_doctor_booked(
        new_doctor,
        new_date,
        new_time,
        exclude_id=appointment_id,
    ):
        return {"error": f"{new_doctor} is already booked on {new_date} at {new_time}"}

    allowed_fields = ["patient_name", "doctor", "date", "time"]

    for field in allowed_fields:
        if field in json_body:
            appointment[field] = json_body[field]

    return {
        "message": "Appointment updated successfully!",
        "appointment": appointment,
    }


@app.delete("/appointments/remove")
async def remove_appointment(appointment_id: int) -> dict:
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    appointments.remove(appointment)

    return {"message": f"Appointment {appointment_id} removed successfully!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
