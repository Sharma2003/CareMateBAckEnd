from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ConsultationNoteCreate(BaseModel):
    session_id : UUID
    note_text : str
    created_by : UUID

class ConsultationNoteResponse(BaseModel):
    id : UUID
    session_id : UUID
    doctor_id : UUID
    created_by : UUID
    note_text : str 
    created_at : datetime