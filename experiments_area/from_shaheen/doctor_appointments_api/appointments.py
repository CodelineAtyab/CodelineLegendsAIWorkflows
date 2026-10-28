appointments: list[dict] = [
  {"id": 1, "patient_name": "Salim", "doctor": "Dr. Aisha", "date": "2026-11-03", "time": "10:30"},
  {"id": 2, "patient_name": "Fatma", "doctor": "Dr. Khalid", "date": "2026-11-03", "time": "11:00"},
  {"id": 3, "patient_name": "Ahmed", "doctor": "Dr. Noor", "date": "2026-11-05", "time": "14:00"}
]


def find_appointment(appointment_id: int) -> dict | None:
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment
    return None


def get_next_id() -> int:
    highest_id = 0
    for appointment in appointments:
        highest_id = max(highest_id, appointment["id"])
    return highest_id + 1


# skip_id lets an appointment being updated keep its own slot
def is_doctor_booked(doctor: str, date: str, time: str, skip_id: int | None = None) -> bool:
    for appointment in appointments:
        if appointment["id"] == skip_id:
            continue
        if appointment["doctor"].lower() == doctor.lower() and appointment["date"] == date and appointment["time"] == time:
            return True
    return False
