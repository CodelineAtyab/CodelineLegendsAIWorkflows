from fastapi import FastAPI

from models.engineer import (
    CivilEngineerRegistration,
    SoftwareEngineerRegistration,
)

app = FastAPI(title="Engineer Registration API")


@app.post("/engineers/software")
def register_software_engineer(engineer: SoftwareEngineerRegistration):
    return {
        "name": engineer.name,
        "email": engineer.email,
        "activity_percent": engineer.activity_percent(),
    }


@app.post("/engineers/civil")
def register_civil_engineer(engineer: CivilEngineerRegistration):
    return {
        "name": engineer.name,
        "email": engineer.email,
        "activity_percent": engineer.activity_percent(),
    }
