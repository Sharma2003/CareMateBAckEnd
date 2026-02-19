from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy.sql import func

from entities.ConsultationSession import ConsultationSession
from entities.Booking import Booking
from entities.ConsultationNotes import ConsultationNotes
from consultation_notes.model import ConsultationNoteCreate, ConsultationNoteResponse

def write_notes(db:Session, payload:ConsultationNoteCreate, consultation_id: UUID, doctor_id : UUID):
    session_existing = db.query(ConsultationSession).filter(ConsultationSession.id == consultation_id).first()
    
    booking_existing = session_existing.booking

    if not session_existing:
        raise HTTPException(status_code=404,detail="Consultation session not found")
    
    if not booking_existing:
        raise HTTPException(status_code=400, detail="Invalid session")
    
    if not booking_existing.doctor_id != doctor_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    note = ConsultationNoteCreate(
        session_id = consultation_id,
        note_text=payload.note_text,
        created_by=doctor_id
    )   
    db.add(note)
    db.commit()
    db.refresh(note)


    return ConsultationNoteResponse.model_validate(note)