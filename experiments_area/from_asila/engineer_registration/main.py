import uvicorn
from fastapi import FastAPI

from models.engineer_registration import SoftwareEngineerRegistration

app = FastAPI()

@app.post("/engineers/software")
def register_software_engineer(
    engineer: SoftwareEngineerRegistration,
) -> dict[str, str | int]:
    return {
        "name": engineer.name,
        "email": engineer.email,
        "activity_percent": engineer.activity_percent(),
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
