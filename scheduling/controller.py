from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from entities.Users import User
from database.core import DbSession
from auth.service import CurrentUser
from scheduling.model import doctorAvailability, doctorAvailabilityResponse
from scheduling.service import create_Doctor_Scheule, get_Doctor_Availability, update_Doctor_Availability, delete_Doctor_Availability
from helper.ensure import ensure_doctor_role, ensure_doctor_facility, ensure_doctor_username

from uuid import UUID

router = APIRouter(
    prefix="/schedule",
    tags=["schedule"]
)

@router.post("/",response_model=doctorAvailabilityResponse)
def create(payload:doctorAvailability, db : DbSession, facility_id : UUID, current_user : CurrentUser):
    ensure_doctor_role(current_user=current_user.get_uuid(), db = db)
    # ensure_doctor_username(db=db , username=current_user.user_id)
    return create_Doctor_Scheule(db=db,doctor_id=current_user.get_uuid(),facility_id=facility_id,payload=payload)
 
@router.get("/")
def get_Availability(db:DbSession, current_user:CurrentUser):
    ensure_doctor_role(current_user=current_user.get_uuid(), db = db)
    # ensure_doctor_username(db=db , username=current_user.user_id)
    return get_Doctor_Availability(db=db,doctor_id=current_user.get_uuid())

@router.put("/{facility_id}",response_model=doctorAvailabilityResponse)
def update_Availability(db:DbSession,facility_id : UUID,current_user : CurrentUser ,payload: doctorAvailability):
    ensure_doctor_role(current_user=current_user.get_uuid(), db = db)
    ensure_doctor_facility(db=db, facility_id=facility_id)
    return update_Doctor_Availability(db=db, facility_id=facility_id, payload=payload)

@router.delete("/delete_Doctor_Availability")
def delete_Availability(db:DbSession,Scheduling_id : UUID, current_user : CurrentUser, facility_id : UUID):
    ensure_doctor_role(db=db, current_user=current_user.get_uuid())
    ensure_doctor_facility(db=db, facility_id=facility_id)
    return delete_Doctor_Availability(db=db, Scheduling_id=Scheduling_id)
