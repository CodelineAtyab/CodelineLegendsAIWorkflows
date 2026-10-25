import uvicorn
from fastapi import FastAPI
from appointments import appointments

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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
