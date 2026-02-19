from pydantic import BaseModel, field_validator, model_validator
from uuid import UUID
from datetime import time, date, datetime
from zoneinfo import ZoneInfo
from typing import Optional
from entities.Booking import BookingStatus

class bookingSlots(BaseModel):
    booking_date : date
    start_ts : time
    end_ts : time    
    status : BookingStatus = BookingStatus.BOOKED

    @model_validator(mode='after')
    def validate_time_order(self):
        if self.end_ts <= self.start_ts:
            raise ValueError("end_ts must be greater than start_ts")
    
        return self

class bookingSlotsResponse(BaseModel):
    id: UUID
    doctor_id: UUID
    patient_id: UUID
    facility_id: UUID
    start_ts: datetime
    end_ts: datetime
    status: BookingStatus

    model_config = {"from_attributes": True}
    