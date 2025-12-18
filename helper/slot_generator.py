import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

    while current_start + timedelta(minutes=duration) <= end_datetime:
        slots.append({
            "start_time": current_start.time(),
            "end_time": (current_start + timedelta(minutes=duration)).time()
        })
        current_start += timedelta(minutes=duration)

    return slots