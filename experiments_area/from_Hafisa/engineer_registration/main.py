import uvicorn
from fastapi import FastAPI

from models.engineer import CivilEngineerRegistration, SoftwareEngineerRegistration

app = FastAPI()


@app.post("/engineers/software")
def register_software(engineer: SoftwareEngineerRegistration) -> dict[str, str | int]:
