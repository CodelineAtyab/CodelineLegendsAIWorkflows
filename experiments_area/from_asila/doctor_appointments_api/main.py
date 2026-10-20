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

def main():
    print("Hello from doctor-appointments-api!")


if __name__ == "__main__":
    main()
