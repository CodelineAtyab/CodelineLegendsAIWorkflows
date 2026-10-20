# Doctor Appointments API

A simple Doctor Appointments API built using Python and FastAPI. It allows users to view, book, update, and remove doctor appointments.

## Features

- **GET** `/appointments` — View all appointments or filter by doctor and date.
- **POST** `/appointments/book` — Book a new appointment.
- **PUT** `/appointments/update` — Update an existing appointment.
- **DELETE** `/appointments/remove` — Remove an appointment.

## Technologies Used

- Python 3.14
- FastAPI
- Uvicorn
- uv

## Project Structure

```text
doctor_appointments_api/
├── main.py
├── appointments.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Installation

Install the dependencies:

```bash
uv sync
```

## Run the Project

Start the API server:

```bash
uv run main.py
```

Open the API documentation in your browser:

http://localhost:8000/docs

## Example: Book an Appointment

Send a POST request to `/appointments/book` with this JSON body:

```json
{
  "patient_name": "Maryam",
  "doctor": "Dr. Aisha",
  "date": "2026-11-04",
  "time": "09:00"
}
```

## Error Handling

The API handles:
- Missing required fields
- Doctor double bookings
- Appointments that do not exist

## Note

Appointments are stored in a Python list, not a database. The data resets when the server restarts.
