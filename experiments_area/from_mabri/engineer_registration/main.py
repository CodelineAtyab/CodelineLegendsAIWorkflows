from fastapi import FastAPI
from models.engineer_model import SoftwareEngineerRegistration, CivilEngineerRegistration
import uvicorn

app = FastAPI()


@app.post("/enginners/software")
def create_software_engineer_registration(registration: SoftwareEngineerRegistration):
    return {name: registration.name, email: registration.email, "activity_percent": registration.activity_percent()}


@app.post("/enginners/civil")
def create_civil_engineer_registration(registration: CivilEngineerRegistration):
    return {name: registration.name, email: registration.email, "activity_percent": registration.activity_percent()}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)