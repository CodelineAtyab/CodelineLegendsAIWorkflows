# Store three sample appointments
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
        "date": "2026-11-04",
        "time": "09:00",
    },
    {
        "id": 3,
        "patient_name": "Ali",
        "doctor": "Dr. Sara",
        "date": "2026-11-05",
        "time": "11:00",
    },
]


# Find appointment by ID
def find_appointment(appointment_id: int) -> dict | None:
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment

    return None


# Generate the next unique appointment ID
def next_id() -> int:
    if not appointments:
        return 1

    return max(appointment["id"] for appointment in appointments) + 1


# Check if doctor is already booked at the same date and time
def is_booked(
    doctor: str,
    date: str,
    time: str,
    exclude_id: int | None = None,
) -> bool:
    for appointment in appointments:
        if (
            appointment["doctor"].lower() == doctor.lower()
            and appointment["date"] == date
            and appointment["time"] == time
            and appointment["id"] != exclude_id
        ):
            return True

    return False
