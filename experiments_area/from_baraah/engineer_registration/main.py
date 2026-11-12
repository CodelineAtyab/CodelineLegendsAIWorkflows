"""FastAPI application for engineer registration."""

import uvicorn
from fastapi import FastAPI

from models.engineer import (
    CivilEngineerRegistration,
    SoftwareEngineerRegistration,
)

app = FastAPI(title="Engineer Registration API")


@app.post("/engineers/software")
def register_software_engineer(
    engineer: SoftwareEngineerRegistration,
) -> dict[str, str | int]:
    """Register a software engineer."""
    return {
        "name": engineer.name,
        "email": engineer.email,
        "activity_percent": engineer.activity_percent(),
    }


@app.post("/engineers/civil")
def register_civil_engineer(
    engineer: CivilEngineerRegistration,
) -> dict[str, str | int]:
    """Register a civil engineer."""
    return {
        "name": engineer.name,
        "email": engineer.email,
        "activity_percent": engineer.activity_percent(),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
