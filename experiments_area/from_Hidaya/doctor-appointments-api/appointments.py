appointments: list[dict] = [
    {
        "id": 1,
        "patient_name": "Omar Haddad",
        "doctor": "Dr. Aisha",
        "date": "2026-11-04",
        "time": "09:00",
    },
    {
        "id": 2,
        "patient_name": "Lina Mansour",
        "doctor": "Dr. Karim",
        "date": "2026-11-04",
        "time": "10:30",
    },
    {
        "id": 3,
        "patient_name": "Yousef Nader",
        "doctor": "Dr. Salma",
        "date": "2026-11-05",
        "time": "11:15",
    },
]

next_id: int = 4


def find_appointment(appointment_id: int) -> dict | None:
    """Find an appointment by its id."""
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment
    return None


def generate_next_id() -> int:
    """Create an id that is never reused during this run."""
    global next_id

    appointment_id = next_id
    next_id += 1
    return appointment_id


def is_doctor_booked(
    doctor: str,
    date: str,
    time: str,
    exclude_id: int | None = None,
) -> bool:
    """Check whether a doctor already has this appointment slot."""
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


def build_conflict_error(doctor: str, date: str, time: str) -> dict:
    """Build the error message for an occupied slot."""
    return {"error": f"{doctor} is already booked on {date} at {time}"}
