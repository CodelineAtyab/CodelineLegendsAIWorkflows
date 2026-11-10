from fastapi import FastAPI

from models.engineer import SoftwareEngineerRegistration

app = FastAPI()


@app.post("/engineers/software")
def register_software_engineer(engineer: SoftwareEngineerRegistration):
    return {
        "name": engineer.name,
        "email": engineer.email,
        "activity_percent": engineer.activity_percent(),
    }