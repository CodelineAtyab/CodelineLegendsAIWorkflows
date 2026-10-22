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


def find_appointment(appointment_id: int) -> dict | None:
    """Find an appointment by its unique identifier."""
    for appt in appointments:
        if appt["id"] == appointment_id:
            return appt
    return None


def get_next_id() -> int:
    """Generate the next appointment ID as highest id + 1."""
    return max((appt["id"] for appt in appointments), default=0) + 1


def is_doctor_booked(
    doctor: str,
    date: str,
    time: str,
    exclude_id: int | None = None,
) -> bool:
    """Check if the doctor already has a booking at the specified slot."""
    for appt in appointments:
        if appt["id"] == exclude_id:
            continue
        if (
            appt["doctor"].lower() == doctor.lower()
            and appt["date"] == date
            and appt["time"] == time
        ):
            return True
    return False
