appointments: list[dict] = [
    {
        "id": 1,
        "patient_name": "Salim",
        "doctor": "Dr. Aisha",
        "date": "2026-11-03",
        "time": "10:30",
    },
    {
        "id": 2,
        "patient_name": "Ahmed",
        "doctor": "Dr. Khalid",
        "date": "2026-11-03",
        "time": "11:00",
    },
    {
        "id": 3,
        "patient_name": "Sara",
        "doctor": "Dr. Fatma",
        "date": "2026-11-04",
        "time": "09:30",
    },
]

last_id = max((appointment["id"] for appointment in appointments), default=0)


def find_appointment(appointment_id: int) -> dict | None:
    """Return the appointment with this ID, or None when it does not exist."""
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment

    return None


def get_next_id() -> int:
    """Create an ID that has not been used during this server run."""
    global last_id
    last_id += 1
    return last_id


def is_doctor_booked(
    doctor: str,
    date: str,
    time: str,
    exclude_id: int | None = None,
) -> bool:
    """Check for a matching booking, optionally excluding the updated appointment."""
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
