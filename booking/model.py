from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import time

class bookingSlots(BaseModel):
    start_ts : time
    end_ts : time 
    status : str

    @field_validator("start_ts", "end_ts",mode="before")
    @classmethod
    def parse_time(cls, v):
        if isinstance(v, str):
            h, m = map(int, v.split(":"))
            return time(h,m)
        
        return v
    

class bookingSlotsResponse(bookingSlots):
    id : UUID
    doctor_id : UUID
    patient_id : UUID
    facility_id : UUID