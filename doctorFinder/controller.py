from doctorFinder.service import list_facilities, list_doctors_by_facility, list_doctor_slots
from fastapi import APIRouter
from database.core import DbSession
from uuid import UUID
from helper.ensure import ensure_patient_role
from auth.service import CurrentUser

router = APIRouter(
    prefix="/DoctorFinder",
    tags=["DoctorFinder"]
)

@router.get("/facility")
def facility(db : DbSession, current_user : CurrentUser):
    ensure_patient_role(db=db, current_user=current_user.get_uuid())
    return list_facilities(db=db)

@router.get("/doctor")
def get_doctors(db: DbSession, facility_id: UUID, current_user: CurrentUser):
    ensure_patient_role(db=db, current_user=current_user.get_uuid())
    return list_doctors_by_facility(db=db, facility_id=str(facility_id))


@router.get("/doctor-slots")
def get_doctor_slots(db: DbSession, doctor_id: UUID, current_user: CurrentUser):
    ensure_patient_role(db=db, current_user=current_user.get_uuid())
    return list_doctor_slots(db=db, doctor_id=str(doctor_id))