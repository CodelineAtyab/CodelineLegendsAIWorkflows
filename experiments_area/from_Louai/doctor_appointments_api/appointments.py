appointments: list[dict] = [
    {
        "id":1,
        "patient_name": "Salim",
        "doctor": "Dr.Louai",
        "date": "2026-11-03",
        "time": "10:30",

    },
    
    {
         "id":2,
        "patient_name": "Mohammed",
        "doctor": "Dr.Ahmed",
        "date": "2026-12-04",
        "time": "11:30",

        
    },

    {
         "id":3,
        "patient_name": "Omar",
        "doctor": "Dr.Sami",
        "date": "2026-11-05",
        "time": "12:30",
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
    highest_id = 0
    for appointment in appointments:
        highest_id = max(highest_id, appointment["id"])
    return highest_id + 1

def is_doctor_booked(doctor: str, date: str, time: str, ignore_id: int | None = None) -> bool:
    for appointment in appointments:
        if appointment["id"] == ignore_id:
            continue
        if (
            appointment["doctor"].lower() == doctor.lower()
            and appointment["date"] == date
            and appointment["time"] == time
        ):
            return True
    return False



