from scheduling.service import get_Doctor_Availability
# from auth.service import CurrentUser
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timedelta, time

def slot_generator(db:Session, current_user : UUID):
    slots = []
    user = get_Doctor_Availability(db=db, doctor_id=current_user)
    start_time = user.start_time
    end_time = user.end_time
    duration = user.slot_duration_minutes
    base_date = datetime.today().date()

    current_start = datetime.combine(base_date, start_time)
    end_datetime = datetime.combine(base_date, end_time)
    print("start_time:", user.start_time)
    print("end_time:", user.end_time)
    print("duration:", user.slot_duration_minutes)
    print("current_start:", current_start)
    print("end_datetime:", end_datetime)
    while current_start + timedelta(minutes=duration) <= end_datetime:
        slots.append({
            "start_time": current_start.time().strftime("%H:%M:%S"),
            "end_time": (current_start + timedelta(minutes=duration)).time().strftime("%H:%M:%S")
        })
        current_start += timedelta(minutes=duration)

    return slots