import uvicorn
import appointments
from fastapi import FastAPI, Request


app = FastAPI()


@app.get("/appointments")
async def get_appointments(doctor: str | None = None, date: str | None = None) -> dict:
    filtered_appointments = appointments.appointments
    if doctor:
        filtered_appointments = [
            appointment
            for appointment in filtered_appointments
            if appointment["doctor"].lower() == doctor.lower()
        ]
    if date:
        filtered_appointments = [
            appointment
            for appointment in filtered_appointments
            if appointment["date"] == date
        ]
    return {"appointments": filtered_appointments, "count": len(filtered_appointments)}


@app.post("/appointments/book")
async def book_appointment(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()
    for field in ["patient_name", "doctor", "date", "time"]:
        if json_body.get(field) is None:
            return {"error": f"Missing field: {field}"}
    doctor = json_body.get("doctor")
    date = json_body.get("date")
    time = json_body.get("time")
    if appointments.is_doctor_booked(doctor, date, time):
        return {"error": f"{doctor} is already booked on {date} at {time}"}
    new_appointment = {"id": appointments.next_id(),"patient_name": json_body.get("patient_name"), "doctor": doctor, "date": date, "time": time}
    appointments.appointments.append(new_appointment)
    return {"message": "Appointment booked successfully!", "appointment": new_appointment}


@app.put("/appointments/update")
async def update_appointment(appointment_id: int, incoming_request: Request) -> dict:
    appointment = appointments.find_appointment(appointment_id)
    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}
    new_data = await incoming_request.json()
    # The slot after the update: sent values win, missing ones keep the current value
    doctor = new_data.get("doctor", appointment["doctor"])
    date = new_data.get("date", appointment["date"])
    time = new_data.get("time", appointment["time"])
    if appointments.is_doctor_booked(doctor, date, time, ignore_id=appointment_id):
        return {"error": f"{doctor} is already booked on {date} at {time}"}
    for field in ["patient_name", "doctor", "date", "time"]:
        if field in new_data:
            appointment[field] = new_data[field]
    return {"message": "Appointment updated successfully!", "appointment": appointment}


@app.delete("/appointments/remove")
async def remove_appointment(appointment_id: int) -> dict:
    appointment = appointments.find_appointment(appointment_id)
    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}
    appointments.appointments.remove(appointment)
    return {"message": f"Appointment {appointment_id} removed successfully!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
