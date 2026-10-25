import uvicorn
from fastapi import FastAPI, Request
from appointments import appointments, find_appointment, get_next_id, is_doctor_booked

app = FastAPI()


@app.get("/appointments")
async def view_appointments(doctor: str | None = None, date: str | None = None) -> dict:
    matching_appointments: list[dict] = []
    for appointment in appointments:
        if doctor is not None and appointment["doctor"].lower() != doctor.lower():
            continue
        if date is not None and appointment["date"] != date:
            continue
        matching_appointments.append(appointment)

    return {"appointments": matching_appointments, "count": len(matching_appointments)}


@app.post("/appointments/book")
async def book_appointment(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    required_fields = ["patient_name", "doctor", "date", "time"]
    for field in required_fields:
        if json_body.get(field) is None:
            return {"error": f"Missing field: {field}"}

    doctor = json_body.get("doctor")
    date = json_body.get("date")
    time = json_body.get("time")
    if is_doctor_booked(doctor, date, time):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    new_appointment = {
        "id": get_next_id(),
        "patient_name": json_body.get("patient_name"),
        "doctor": doctor,
        "date": date,
        "time": time
    }
    appointments.append(new_appointment)
    return {"message": "Appointment booked successfully!", "appointment": new_appointment}


@app.put("/appointments/update")
async def update_appointment(appointment_id: int, incoming_request: Request) -> dict:
    appointment = find_appointment(appointment_id)
    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    json_body = await incoming_request.json()

    doctor = json_body.get("doctor", appointment["doctor"])
    date = json_body.get("date", appointment["date"])
    time = json_body.get("time", appointment["time"])
    if is_doctor_booked(doctor, date, time, skip_id=appointment_id):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    allowed_fields = ["patient_name", "doctor", "date", "time"]
    for key in json_body:
        if key in allowed_fields:
            appointment[key] = json_body[key]

    return {"message": "Appointment updated successfully!", "appointment": appointment}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
