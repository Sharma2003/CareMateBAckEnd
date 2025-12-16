
from pydantic import BaseModel
from uuid import UUID
from datetime import date, time

class doctorAvailability(BaseModel):
    day_of_week : int
    start_time : time
    end_time : time
    slot_duration_minutes : int
    is_active : bool


class doctorAvailabilityResponse(doctorAvailability):
    id : UUID
    facility_id : UUID
    doctor_id : UUID

    class Config:
        orm_mode = True