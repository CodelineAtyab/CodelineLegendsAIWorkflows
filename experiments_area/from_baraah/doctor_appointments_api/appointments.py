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


# Find an appointment by ID
def find_appointment(appointment_id: int) -> dict | None:
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment

    return None


def next_appointment_id() -> int:
    highest_id = 0

    for appointment in appointments:
        if appointment["id"] > highest_id:  # noqa: PLR1730
            highest_id = appointment["id"]

    return highest_id + 1


# Check if a doctor is already booked
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
