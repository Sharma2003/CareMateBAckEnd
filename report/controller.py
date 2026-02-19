from fastapi import APIRouter, HTTPException

from database.core import DbSession
from auth.service import CurrentUser
from helper.ensure import ensure_patient_role, ensure_doctor_role
from report.service import get_patient_report, get_doctor_report


router = APIRouter(
    prefix="/report",
    tags=["report"]
)


@router.get("/patient-report")
def get_report(db:DbSession,current_user:CurrentUser):
    ensure_patient_role(db=db,current_user=current_user.get_uuid())
    return get_patient_report(db=db,patient_id=current_user.get_uuid())

@router.get("/doctor-report")
def get_report(db:DbSession, current_user : CurrentUser):
    ensure_doctor_role(db=db,current_user=current_user.get_uuid())
    return get_doctor_report(db=db, doctor_id=current_user.get_uuid())
