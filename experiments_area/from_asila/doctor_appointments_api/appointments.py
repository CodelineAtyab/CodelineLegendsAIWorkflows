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
        "doctor": "Dr. Ahmed",
        "date": "2026-11-03",
        "time": "11:00",
    },
    {
        "id": 3,
        "patient_name": "Ali",
        "doctor": "Dr. Sara",
        "date": "2026-11-04",
        "time": "09:00",
    },
]


# finds an appointment by id and returns it or None
def find_appointment(appointment_id: int) -> dict | None:
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment

    return None


# creates the next id
def get_next_id() -> int:
    highest_id = 0

    for appointment in appointments:
        highest_id = max(highest_id, appointment["id"])

    return highest_id + 1


# booking-check
def is_doctor_booked(
    doctor: str,
    date: str,
    time: str,
    appointment_id: int | None = None,
) -> bool:
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            continue

        if (
            appointment["doctor"].lower() == doctor.lower()
            and appointment["date"] == date
            and appointment["time"] == time
        ):
            return True

    return False
