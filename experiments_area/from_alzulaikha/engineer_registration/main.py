from fastapi import FastAPI
from models.engineer import (
    SoftwareEngineerRegistration,
    CivilEngineerRegistration
)
app = FastAPI(
title="Engineer Registration API",
description="API for registering engineers and calculating their activity percentage",
version="1.0.0",
)
@app.post("/engineers/software")
def register_software_engineer(
    engineer: SoftwareEngineerRegistration
):
    return {
        "name": engineer.name,
        "email": engineer.email,
        "activity_percent": engineer.activity_percent()
    }
@app.post("/engineers/civil")
def register_civil_engineer(
    engineer: CivilEngineerRegistration
):
    return {
        "name": engineer.name,
        "email": engineer.email,
        "activity_percent": engineer.activity_percent()
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)