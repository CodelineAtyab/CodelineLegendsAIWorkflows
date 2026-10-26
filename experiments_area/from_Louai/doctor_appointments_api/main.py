import uvicorn
from fastapi import FastAPI, Request

from appointments import appointments, find_appointment, get_next_id, is_doctor_booked

app = FastAPI()


@app.get("/appointments")
async def view_appointments(doctor: str | None = None, date: str | None = None) -> dict:
    results = []
    for appointment in appointments:
        if doctor is not None and appointment["doctor"].lower() != doctor.lower():
            continue
        if date is not None and appointment["date"] != date:
            continue
        results.append(appointment)
    return {"appointments": results, "count": len(results)}


@app.post("/appointments/book")
async def book_appointment(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    required_fields = ["patient_name", "doctor", "date", "time"]
    for field in required_fields:
        if json_body.get(field) is None:
            return {"error": f"Missing field: {field}"}

    doctor = json_body["doctor"]
    date = json_body["date"]
    time = json_body["time"]

    if is_doctor_booked(doctor, date, time):
        return {"error": f"{doctor} is already booked on {date} at {time}"}

    new_appointment = {
        "id": get_next_id(),
        "patient_name": json_body["patient_name"],
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

    json_body = await incoming_request.json()

    new_doctor = json_body.get("doctor", appointment["doctor"])
    new_date = json_body.get("date", appointment["date"])
    new_time = json_body.get("time", appointment["time"])

    if is_doctor_booked(new_doctor, new_date, new_time, ignore_id=appointment_id):
        return {"error": f"{new_doctor} is already booked on {new_date} at {new_time}"}

    for key in ["patient_name", "doctor", "date", "time"]:
        if key in json_body:
            appointment[key] = json_body[key]

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