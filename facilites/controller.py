from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID
from database.core import DbSession
from facilites.service import create_doctor_facility, get_facility, update_facility, delete_facility
from facilites.model import FacilitiesDetails, FacilityResponse
from auth.service import CurrentUser
from entities.Users import User
from entities.FacilityMaster import Facility
from helper.ensure import ensure_doctor_role, ensure_doctor_username


router = APIRouter(
    prefix="/facilities",
    tags=["facilities"]
)


@router.post("/",response_model=FacilityResponse)
def create(current_user : CurrentUser, payload : FacilitiesDetails, db : DbSession):
    ensure_doctor_role(db=db, current_user=current_user.get_uuid())
    return create_doctor_facility(db=db, payload=payload, doctor_id=current_user.get_uuid())

@router.get("/get_facility")
def get_facility_by_id(current_user : CurrentUser ,db : DbSession):
    ensure_doctor_role(db=db, current_user=current_user.get_uuid())
    # ensure_doctor_username(db=db, username=current_user.user_id)
    return get_facility(current_user=current_user.get_uuid(), db=db)

@router.put("/update_facility/{facility_id}",response_model=FacilityResponse)
def update(facility_id : UUID,current_user : CurrentUser, db : DbSession, payload : FacilitiesDetails):
    ensure_doctor_role(db=db, current_user=current_user.get_uuid())
    # ensure_doctor_username(db=db, username=current_user.user_id)
    return update_facility(facility_id=facility_id, db=db, payload=payload)

@router.delete("/delete_facility/{facility_id}")
def delete(facility_id : UUID, db : DbSession, current_user : CurrentUser):
    ensure_doctor_role(db=db, current_user=current_user.get_uuid())
    return delete_facility(db=db, facility_id=facility_id)