
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
        "patient_name": "Sara",
        "doctor": "Dr. Khalid",
        "date": "2026-11-03",
        "time": "11:00",
    },
    {
        "id": 3,
        "patient_name": "Ahmed",
        "doctor": "Dr. Aisha",
        "date": "2026-11-04",
        "time": "09:00",
    },
]


def find_appointment(appointment_id: int) -> dict | None:
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment

    return None


def create_next_id() -> int:
    if not appointments:
        return 1

    highest_id = max(appointment["id"] for appointment in appointments)
    return highest_id + 1


def is_doctor_booked(
    doctor: str,
    date: str,
    time: str,
    exclude_id: int | None = None,
) -> bool:
    for appointment in appointments:
        if appointment["id"] == exclude_id:
            continue

        same_doctor = appointment["doctor"].lower() == doctor.lower()
        same_date = appointment["date"] == date
        same_time = appointment["time"] == time

        if same_doctor and same_date and same_time:
            return True

    return False
