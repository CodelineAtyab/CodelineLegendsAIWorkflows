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
        "patient_name": "Maryam",
        "doctor": "Dr. Khalid",
        "date": "2026-11-04",
        "time": "09:00",
    },
    {
        "id": 3,
        "patient_name": "Ahmed",
        "doctor": "Dr. Aisha",
        "date": "2026-11-05",
        "time": "11:00",
    },
]


def find_appointment(appointment_id: int) -> dict | None:
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment

    return None


def get_next_id() -> int:
    if not appointments:
        return 1

    return max(appointment["id"] for appointment in appointments) + 1


def is_doctor_booked(
    doctor: str,
    date: str,
    time: str,
    exclude_id: int | None = None,
) -> bool:
    for appointment in appointments:
        if appointment["id"] == exclude_id:
            continue

        if (
            appointment["doctor"].casefold() == doctor.casefold()
            and appointment["date"] == date
            and appointment["time"] == time
        ):
            return True

    return False
