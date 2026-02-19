from pydantic import BaseModel
from typing import Literal
from datetime import datetime
from uuid import UUID 
from entities.ConsultationSession import SessionType, SessionStatus

class ConsultationSessionCreate(BaseModel):
    booking_id : UUID
    session_type : SessionType

class ConsultationSessionResponse(BaseModel):
    id : UUID
    booking_id :UUID
    session_type : SessionType
    status : SessionStatus
    start_time : datetime
    end_time : datetime | None = None

    model_config = {"from_attributes": True}