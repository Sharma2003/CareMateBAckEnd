import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.core import DbSession
from auth.service import CurrentUser
from entities.DoctorFacility import DoctorAvailability
from entities.FacilityMaster import Facility
from entities.Doctor import Doctor
from scheduling.model import doctorAvailability, doctorAvailabilityResponse
from scheduling.service import create_Doctor_Scheule, get_Doctor_Availability, update_Doctor_Availability, delete_Doctor_Availability
from uuid import UUID

router = APIRouter(
    prefix="/schedule",
    tags=["schedule"]
)

def ensure_Doctor(db : Session, current_user : UUID):
    user = db.query(DoctorAvailability).filter(DoctorAvailability.doctor_id == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/create",response_model=doctorAvailabilityResponse)
def create(payload:doctorAvailability, db : DbSession, facility_id : UUID, current_id : CurrentUser):
    return create_Doctor_Scheule(db=db,doctor_id=current_id.get_uuid(),facility_id=facility_id,payload=payload)

@router.get("/get_Doctor_Availability")
def get_Availability(db:DbSession, current_user:CurrentUser):
    return get_Doctor_Availability(db=db,doctor_id=current_user.get_uuid())

@router.put("/update_Doctor_Availability",response_model=doctorAvailabilityResponse)
def update_Availability(db:DbSession,facility_id : UUID, payload: doctorAvailability):
    return update_Doctor_Availability(db=db, facility_id=facility_id, payload=payload)

@router.delete("/delete_Doctor_Availability",response_model=doctorAvailabilityResponse)
def delete_Availability(db:DbSession,Scheduling_id : UUID, current_user : CurrentUser):
    ensure_Doctor(db=db, current_user=current_user.get_uuid())
    return delete_Doctor_Availability(db=db, Scheduling_id=Scheduling_id)
