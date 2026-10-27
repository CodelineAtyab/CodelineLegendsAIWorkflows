import uvicorn
from fastapi import FastAPI, Request

from appointments import appointments, find_appointment, get_next_id, is_doctor_booked

app = FastAPI()

ALLOWED_UPDATE_FIELDS = ("patient_name", "doctor", "date", "time")


@app.get("/appointments")
async def view_appointments(
    doctor: str | None = None,
    date: str | None = None,
) -> dict[str, list[dict] | int]:
    matching_appointments = [
        appointment
        for appointment in appointments
        if (doctor is None or str(appointment["doctor"]).lower() == doctor.lower())
        and (date is None or appointment["date"] == date)
    ]
    return {"appointments": matching_appointments, "count": len(matching_appointments)}


@app.post("/appointments/book")
async def book_appointment(request: Request) -> dict:
    json_body = await request.json()

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
    return {"message": "Appointment booked successfully!", "appointment": appointment}


@app.put("/appointments/update")
async def update_appointment(appointment_id: int, request: Request) -> dict:
    json_body = await request.json()
    appointment = find_appointment(appointment_id)
    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    proposed_appointment = appointment.copy()
    for field in ALLOWED_UPDATE_FIELDS:
        if field in json_body:
            proposed_appointment[field] = json_body[field]

    if is_doctor_booked(
        str(proposed_appointment["doctor"]),
        str(proposed_appointment["date"]),
        str(proposed_appointment["time"]),
        exclude_id=appointment_id,
    ):
        doctor = proposed_appointment["doctor"]
        date = proposed_appointment["date"]
        time = proposed_appointment["time"]
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    appointment.update(proposed_appointment)
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
