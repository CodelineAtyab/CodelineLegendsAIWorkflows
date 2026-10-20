# Store appointments in a list
appointments: list[dict] = [
    {
        "id": 1,
        "patient_name": "Ahmed",
        "doctor": "Dr. Rahaf",
        "date": "2026-11-14",
        "time": "10:30",
    },
    {
        "id": 2,
        "patient_name": "Sarah",
        "doctor": "Dr. Mohammed",
        "date": "2026-11-22",
        "time": "12:00",
    },
    {
        "id": 3,
        "patient_name": "Hafisa",
        "doctor": "Dr. Baraah",
        "date": "2026-11-10",
        "time": "08:00",
    },
]

last_id = 3


# Find an appointment by ID
def find_appointment(appointment_id: int) -> dict | None:
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment
    return None


# Create a unique appointment ID
def next_appointment_id() -> int:
    global last_id

    highest_id = max(
        (appointment["id"] for appointment in appointments),
        default=0,
    )
    last_id = max(last_id, highest_id) + 1

    return last_id


# Check if the doctor is already booked
def doctor_is_booked(
    doctor: str,
    date: str,
    time: str,
    exclude_id: int | None = None,
) -> bool:
    for appointment in appointments:
        if appointment["id"] == exclude_id:
            continue

        if (
            appointment["doctor"].lower() == doctor.lower()
            and appointment["date"] == date
            and appointment["time"] == time
        ):
            return True

    return False
