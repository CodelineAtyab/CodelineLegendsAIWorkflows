Appointment = dict[str, str | int]

appointments: list[Appointment] = [
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

_last_id = max((int(appointment["id"]) for appointment in appointments), default=0)


def find_appointment(appointment_id: int) -> Appointment | None:
    """Return an appointment by ID, or None when it does not exist."""
    return next(
        (
            appointment
            for appointment in appointments
            if appointment["id"] == appointment_id
        ),
        None,
    )


def get_next_id() -> int:
    """Return the next ID without reusing IDs deleted during this server run."""
    global _last_id
    _last_id += 1
    return _last_id


def is_doctor_booked(
    doctor: str,
    date: str,
    time: str,
    exclude_id: int | None = None,
) -> bool:
    """Return whether a doctor has another appointment in the requested slot."""
    return any(
        appointment["id"] != exclude_id
        and str(appointment["doctor"]).lower() == doctor.lower()
        and appointment["date"] == date
        and appointment["time"] == time
        for appointment in appointments
    )
