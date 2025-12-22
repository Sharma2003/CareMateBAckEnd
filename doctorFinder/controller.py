from doctorFinder.service import get_factility, get_doctor
from fastapi import APIRouter
from database.core import DbSession
from uuid import UUID
from helper.slot_generator import slot_generator
from helper.ensure import ensure_patient_role
from auth.service import CurrentUser

router = APIRouter(
    prefix="/DoctorFinder",
    tags=["DoctorFinder"]
)

@router.get("/facility")
def facility(db : DbSession, current_user : CurrentUser):
    ensure_patient_role(db=db, current_user=current_user.get_uuid())
    return get_factility(db=db)

@router.get("/doctor")
def doctor(db: DbSession, facilityname: str, current_user : CurrentUser):
    ensure_patient_role(db=db, current_user=current_user.get_uuid())
    return get_doctor(db=db, facilityname=facilityname)


@router.get("/doctor-slots")
def doctor_slots(db:DbSession, current_user : CurrentUser, id : UUID):
    ensure_patient_role(db=db, current_user=current_user.get_uuid())
    return slot_generator(db=db, current_user=id)
