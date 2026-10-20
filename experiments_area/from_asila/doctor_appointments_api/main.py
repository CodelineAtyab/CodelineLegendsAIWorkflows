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


#added server startup
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
