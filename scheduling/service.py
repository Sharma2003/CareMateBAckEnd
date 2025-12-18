import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID

from entities.DoctorFacility import DoctorAvailability
from entities.Doctor import Doctor
from entities.FacilityMaster import Facility
from helper.ensure import ensure_doctor_role
from scheduling.model import doctorAvailability, doctorAvailabilityResponse

def create_Doctor_Scheule(db:Session, doctor_id : UUID, facility_id : UUID,payload : doctorAvailability)->doctorAvailabilityResponse:
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="No Facility Details Found")
         
    doctor_available=DoctorAvailability(
        facility_id = facility_id,
        doctor_id = doctor_id,
        day_of_week = payload.day_of_week,
        start_time = payload.start_time,
        slot_duration_minutes = payload.slot_duration_minutes,
        end_time = payload.end_time,
        is_active = True
    )

    db.add(doctor_available)
    db.commit()
    db.refresh(doctor_available)

    return DoctorAvailability(
        id = doctor_available.id,
        facility_id = facility_id,
        doctor_id = doctor_id,
        day_of_week = doctor_available.day_of_week,
        start_time = doctor_available.start_time,
        end_time = doctor_available.end_time,
        slot_duration_minutes = doctor_available.slot_duration_minutes,
        is_active = doctor_available.is_active
    )


def get_Doctor_Availability(db:Session, doctor_id: UUID) -> doctorAvailabilityResponse:
    doc = db.query(DoctorAvailability).filter(DoctorAvailability.doctor_id == doctor_id).all()
    if not doc:
        raise HTTPException(status_code=404, detail="doctor id not found")
    return doc

def update_Doctor_Availability(db:Session, facility_id : UUID, payload: doctorAvailability) -> doctorAvailabilityResponse:
    doctor = db.query(DoctorAvailability).filter(DoctorAvailability.facility_id == facility_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="No Facility Details Found")
    
    doctor.day_of_week = payload.day_of_week
    doctor.start_time = payload.start_time
    doctor.end_time = payload.end_time
    doctor.slot_duration_minutes = payload.slot_duration_minutes
    doctor.is_active = payload.is_active
    db.commit()
    return doctor

def delete_Doctor_Availability(db : Session, current_user: UUID, Scheduling_id: UUID):
    user = ensure_doctor_role(current_user=current_user, db = db)
    id = db.query(user).filter(user.id == Scheduling_id).delete()
    if not id:
        raise HTTPException(status_code=404, detail="Scheduling id Not Found") 
    db.commit()
    return id