import uvicorn
from fastapi import FastAPI, Request

#brings the function from appointments.py file
from appointments import (
    appointments,
    find_appointment,
    get_next_id,
    is_doctor_booked,
)

app = FastAPI()

#Add the view action
#it worked with this URL: http://localhost:8000/appointments it will appear appointments
#it i want for a specific one http://localhost:8000/appointments?doctor=dr.%20aisha
@app.get("/appointments")
async def view_appointments(
    doctor: str | None = None,
    date: str | None = None,
) -> dict:
    results: list[dict] = []

    for appointment in appointments:
        if doctor is not None:
            if appointment["doctor"].lower() != doctor.lower():
                continue

        if date is not None:
            if appointment["date"] != date:
                continue

        results.append(appointment)

    return {"appointments": results, "count": len(results)}

#to do post and put we need to open the server in wsl terminal and then open another wsl terminal to do the post and put during the server running


#Added post action that adds a new appointment with a new id and returns it
#ex to do post in terminal: curl -X POST http://localhost:8000/appointments/book -H "Content-Type: application/json" -d '{"patient_name":"Maryam","doctor":"Dr. Aisha","date":"2026-11-04","time":"09:00"}'
@app.post("/appointments/book")
async def book_appointment(incoming_request: Request) -> dict:
    json_body = await incoming_request.json()

    required_fields = ["patient_name", "doctor", "date", "time"]

    for field in required_fields:
        if json_body.get(field) is None:
            return {"error": f"Missing field: {field}"}

    patient_name = json_body.get("patient_name")
    doctor = json_body.get("doctor")
    date = json_body.get("date")
    time = json_body.get("time")

    if is_doctor_booked(doctor, date, time):
        return {
            "error": f"{doctor} is already booked on {date} at {time}"
        }

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


# to update and Changes only the fields that were sent and returns the updated appointment
#ex to do put in terminal : curl -X PUT "http://localhost:8000/appointments/update?appointment_id=4" -H "Content-Type: application/json" -d '{"time":"11:00"}'
@app.put("/appointments/update")
async def update_appointment(
    appointment_id: int,
    incoming_request: Request,
) -> dict:
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    json_body = await incoming_request.json()

    doctor = appointment["doctor"]
    date = appointment["date"]
    time = appointment["time"]

    if "doctor" in json_body:
        doctor = json_body["doctor"]

    if "date" in json_body:
        date = json_body["date"]

    if "time" in json_body:
        time = json_body["time"]

    if is_doctor_booked(doctor, date, time, appointment_id):
        return {
            "error": f"{doctor} is already booked on {date} at {time}"
        }

    allowed_fields = ["patient_name", "doctor", "date", "time"]

    for field in json_body:
        if field in allowed_fields:
            appointment[field] = json_body[field]

    return {
        "message": "Appointment updated successfully!",
        "appointment": appointment,
    }

#added remove action
#ex to do delete in terminal: curl -X DELETE "http://localhost:8000/appointments/remove?appointment_id=3"
@app.delete("/appointments/remove")
async def remove_appointment(appointment_id: int) -> dict:
    appointment = find_appointment(appointment_id)

    if appointment is None:
        return {"error": f"Appointment {appointment_id} not found"}

    appointments.remove(appointment)

    return {
        "message": f"Appointment {appointment_id} removed successfully!"
    }
    
    
    
#added server startup
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
