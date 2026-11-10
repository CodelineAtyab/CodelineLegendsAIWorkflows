import uvicorn
from fastapi import FastAPI

from models.engineer import CivilEngineerRegistration, SoftwareEngineerRegistration

app = FastAPI()


@app.post("/engineers/software")
def register_software(engineer: SoftwareEngineerRegistration) -> dict[str, str | int]:
    return {
        "name": engineer.name,
        "email": engineer.email,
        "activity_percent": engineer.activity_percent(),
    }


@app.post("/engineers/civil")
def register_civil(engineer: CivilEngineerRegistration) -> dict[str, str | int]:
    return {
        "name": engineer.name,
        "email": engineer.email,
