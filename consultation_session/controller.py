from fastapi import APIRouter
from auth.service import CurrentUser
from database.core import DbSession
from uuid import UUID

from helper.ensure import ensure_doctor_role
from consultation_session.service import create_session, close_session, get_session_for_patients
from consultation_session.model import ConsultationSessionResponse, ConsultationSessionCreate
router = APIRouter(
    prefix= "/consultation",
    tags=['consultation-session']
)

@router.post("/create-consultation",response_model=ConsultationSessionResponse)
def start_session(db:DbSession, current_user:CurrentUser,payload:ConsultationSessionCreate):
    ensure_doctor_role(db=db,current_user=current_user.get_uuid())
    return create_session(db=db,payload=payload,doctor_id=current_user.get_uuid())

@router.post("/end-consultation",response_model=ConsultationSessionResponse)
def end_session(db:DbSession,current_user : CurrentUser, session_id:UUID):
    ensure_doctor_role(db=db,current_user=current_user.get_uuid())
    return close_session(db=db, consultation_id=session_id)
    
@router.get("/get-all-session")
def get_session(db:DbSession, current_user : CurrentUser, patient_id : UUID):
    ensure_doctor_role(db=db, current_user=current_user.get_uuid())
    return get_session_for_patients(db=db, patient_id=patient_id)