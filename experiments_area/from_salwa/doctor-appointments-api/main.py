import uvicorn
from fastapi import FastAPI

from appointments import (
    appointments,
    find_appointment,
    get_next_id,
    is_doctor_booked,
)

app = FastAPI()


# 1. View appointments
@app.get("/appointments")
async def view_appointments(
    doctor: str | None = None,
    date: str | None = None,
) -> dict:
    result = []

    for appointment in appointments:
        if doctor is not None and appointment["doctor"].casefold() != doctor.casefold():
            continue

        if date is not None and appointment["date"] != date:
            continue

        result.append(appointment)

    return {
        "appointments": result,
        "count": len(result),
    }


# 2. Book an appointment
@app.post("/appointments/book")
async def book_appointment(json_body: dict) -> dict:
    required_fields = [
        "patient_name",
        "doctor",
        "date",
        "time",
    ]

    for field in required_fields:
        if field not in json_body or json_body[field] is None:
            return {"error": f"Missing field: {field}"}

    patient_name = json_body["patient_name"]
    doctor = json_body["doctor"]
    date = json_body["date"]
    time = json_body["time"]

    if is_doctor_booked(doctor, date, time):
        return {"error": (f"{doctor} is already booked on {date} at {time}")}

    new_appointment = {
        "id": get_next_id(),
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


# 3. Update an appointment
@app.put("/appointments/update")
async def update_appointment(
    appointment_id: int,
    json_body: dict,
) -> dict:
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    allowed_fields = [
        "patient_name",
        "doctor",
        "date",
        "time",
    ]

    updates = {
        field: json_body[field] for field in allowed_fields if field in json_body
    }

    new_doctor = updates.get("doctor", appointment["doctor"])
    new_date = updates.get("date", appointment["date"])
    new_time = updates.get("time", appointment["time"])

    if is_doctor_booked(
        new_doctor,
        new_date,
        new_time,
        exclude_id=appointment_id,
    ):
        return {
            "error": (f"{new_doctor} is already booked on {new_date} at {new_time}")
        }

    appointment.update(updates)

    return {
        "message": "Appointment updated successfully!",
        "appointment": appointment,
    }


# 4. Remove an appointment
@app.delete("/appointments/remove")
async def remove_appointment(
    appointment_id: int,
) -> dict:
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    appointments.remove(appointment)

    return {"message": (f"Appointment {appointment_id} removed successfully!")}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
