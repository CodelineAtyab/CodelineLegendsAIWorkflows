import uvicorn
from fastapi import FastAPI, Request

#brings the function from appointments.py file
from appointments import (
    appointments,
    find_appointment,
    get_next_id,
    is_doctor_booked,
)

app = FastAPI()
def main():
    print("Hello from doctor-appointments-api!")


if __name__ == "__main__":
    main()
