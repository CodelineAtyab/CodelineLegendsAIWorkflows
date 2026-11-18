appointments: list[dict] = [
    {"id": 1, "patient_name": "Salim", "doctor": "Dr. Aisha", "date": "2026-11-03", "time": "10:30"},
    {"id": 2, "patient_name": "Fatma", "doctor": "Dr. Khalid", "date": "2026-11-03", "time": "11:00"},
    {"id": 3, "patient_name": "Ahmed", "doctor": "Dr. Noor", "date": "2026-11-05", "time": "09:30"},
]


def find_appointment(appointment_id: int) -> dict | None:
    """Return appointment dict by id or None if not found."""
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment
    return None


def next_id() -> int:
    """Get the next available appointment id."""
    if not appointments:
        return 1
    return max(a["id"] for a in appointments) + 1


def is_doctor_booked(doctor: str, date: str, time: str, ignore_id: int | None = None) -> bool:
    """Check if doctor is booked at the date and time, ignoring the given appointment id."""
    doctor_lower = doctor.lower()
    for appointment in appointments:
        if ignore_id is not None and appointment["id"] == ignore_id:
            continue
        if (
            appointment["doctor"].lower() == doctor_lower
            and appointment["date"] == date
            and appointment["time"] == time
        ):
            return True
    return False
