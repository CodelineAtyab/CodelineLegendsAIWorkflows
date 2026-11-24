import uvicorn
from fastapi import FastAPI

from models import (
    CivilEngineerRegistration,
    EngineerRegistration,
    SoftwareEngineerRegistration,
)

app = FastAPI(title="Engineer Registration API")


def build_summary(engineer: EngineerRegistration) -> dict:
    return {
        "name": engineer.name,
        "email": engineer.email,
        "activity_percent": engineer.activity_percent(),
    }


@app.post("/engineers/software")
def register_software_engineer(engineer: SoftwareEngineerRegistration) -> dict:
    return build_summary(engineer)


@app.post("/engineers/civil")
def register_civil_engineer(engineer: CivilEngineerRegistration) -> dict:
    return build_summary(engineer)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
