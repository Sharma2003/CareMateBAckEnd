from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy.sql import func

from entities.Booking import Booking
from entities.ConsultationSession import ConsultationSession, SessionStatus
from consultation_session.model import ConsultationSessionCreate, ConsultationSessionResponse

def create_session(db:Session, payload:ConsultationSessionCreate, doctor_id : UUID):
    booking = db.query(Booking).filter(Booking.id == payload.booking_id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="booking not confirmed")
    
    if booking.doctor_id != doctor_id:
        raise HTTPException(status_code=403, detail="Not Authorized")
    
    if booking.status != "booked":
        raise HTTPException(status_code=400, detail="Booking not active")
    

    existing_session = db.query(ConsultationSession).filter(
        ConsultationSession.booking_id == payload.booking_id
        ).first()
    
    if existing_session:
        raise HTTPException(status_code=400, detail="Session already created")
    
    session = ConsultationSession(
        booking_id = payload.booking_id,
        session_type = payload.session_type
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return ConsultationSessionResponse.model_validate(session)

def close_session(db:Session, consultation_id: UUID):
    session = db.query(ConsultationSession).filter(ConsultationSession.id == consultation_id).first()

    if not session:
        raise HTTPException(status_code=404,detail="consultation session not found")
    
    if session.status == SessionStatus.completed:
        raise HTTPException(status_code=400, detail="already completed")
    
    session.end_time = func.now()
    session.status = SessionStatus.completed
    db.add(session)
    db.commit()
    db.refresh(session)

    return ConsultationSessionResponse.model_validate(session)


def get_session_for_patients(db:Session, patient_id:UUID):
    session = db.query(ConsultationSession)\
    .join(Booking)\
    .filter(Booking.patient_id == patient_id)\
    .order_by(ConsultationSession.start_time.desc())\
    .all()

    return session 


def get_session_for_consultation(db:Session, session_id : UUID):
    session = db.query(ConsultationSession).filter(ConsultationSession.id == session_id).first()
    return session