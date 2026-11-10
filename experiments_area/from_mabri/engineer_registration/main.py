from fastapi import FastAPI
from models.engineer_model import SoftwareEngineerRegistration, CivilEngineerRegistration
import uvicorn

app = FastAPI()


@app.post("/engineers/software")
def create_software_engineer_registration(registration: SoftwareEngineerRegistration) -> dict:
    return { "name": registration.name, "email": registration.email, "activity_percent": registration.activity_percent() }


@app.post("/engineers/civil")
def create_civil_engineer_registration(registration: CivilEngineerRegistration) -> dict:
    return { "name": registration.name, "email": registration.email, "activity_percent": registration.activity_percent() }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)