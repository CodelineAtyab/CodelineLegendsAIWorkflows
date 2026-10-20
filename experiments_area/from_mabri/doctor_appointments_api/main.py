import uvicorn
from fastapi import FastAPI
import appointments


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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
