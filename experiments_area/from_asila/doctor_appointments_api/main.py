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


#Added post action that adds a new appointment with a new id and returns it
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






#added server startup
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
