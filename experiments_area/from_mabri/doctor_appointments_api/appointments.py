appointments: list[dict] = [
    {
        "id": 1,
        "patient_name": "Salim",
        "doctor": "Dr. Aisha",
        "date": "2026-11-03",
        "time": "10:30"
    },
    {
        "id": 2,
        "patient_name": "Ahmed",
        "doctor": "Dr. Khalifa",
        "date": "2026-11-11",
        "time": "12:30"
    },
    {
        "id": 3,
        "patient_name": "Fatima",
        "doctor": "Dr. Huda",
        "date": "2026-10-31",
        "time": "08:00"
    }
]


def find_appointment(appointment_id: int) -> dict | None:
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment
    return None


def next_id() -> int:
    if len(appointments) == 0:
        return 1
    return max(appointment["id"] for appointment in appointments) + 1


def is_doctor_booked(doctor: str, date: str, time: str, ignore_id: int | None = None) -> bool:
    for appointment in appointments:
        # Lets an update keep its own slot without clashing with itself
        if appointment["id"] == ignore_id:
            continue
        if (
            appointment["doctor"].lower() == doctor.lower()
            and appointment["date"] == date
            and appointment["time"] == time
        ):
            return True
    return False
