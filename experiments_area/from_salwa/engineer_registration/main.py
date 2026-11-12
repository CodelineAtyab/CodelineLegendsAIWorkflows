
from fastapi import FastAPI
import uvicorn

from models.engineer import (
    SoftwareEngineerRegistration,
    CivilEngineerRegistration,
)


app = FastAPI(title="Engineer Registration API")


@app.post("/engineers/software")
async def register_software_engineer(
    engineer: SoftwareEngineerRegistration,
):
    return {
        "name": engineer.name,
        "email": engineer.email,
        "activity_percent": engineer.activity_percent(),
    }


@app.post("/engineers/civil")
async def register_civil_engineer(
    engineer: CivilEngineerRegistration,
):
    return {
        "name": engineer.name,
        "email": engineer.email,
        "activity_percent": engineer.activity_percent(),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
