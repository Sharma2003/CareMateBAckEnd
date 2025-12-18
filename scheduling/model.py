
from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import time

class doctorAvailability(BaseModel):
    day_of_week: int
    start_time: time
    end_time: time
    slot_duration_minutes: int
    is_active: bool

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_time(cls, v):
        if isinstance(v, str):
            h, m = map(int, v.split(":"))
            return time(h, m)
        return v




class doctorAvailabilityResponse(doctorAvailability):
    id : UUID
    facility_id : UUID
    doctor_id : UUID

    class Config:
        from_attributes = True