from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID

from entities.DoctorFacility import DoctorAvailability
from entities.Doctor import Doctor
from entities.FacilityMaster import Facility
from helper.ensure import ensure_doctor_role
from scheduling.model import doctorAvailability, doctorAvailabilityResponse
from helper.TimeConstraints import _add_minutes_to_time

def create_Doctor_Scheule(db:Session, doctor_id : UUID, facility_id : UUID,payload : doctorAvailability)->doctorAvailabilityResponse:
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="No Facility Details Found")
    
    end_time = _add_minutes_to_time(payload.start_time, payload.slot_duration_minutes)
    doctor_available=DoctorAvailability(
        facility_id = facility_id,
        doctor_id = doctor_id,
        day_of_week = payload.day_of_week,
        start_time = payload.start_time,
        end_time = end_time,
        slot_duration_minutes = payload.slot_duration_minutes,
        is_active = True
    )

    db.add(doctor_available)
    db.commit()
    db.refresh(doctor_available)
    
    return doctorAvailabilityResponse.model_validate(doctor_available)

def get_Doctor_Availability(db:Session, doctor_id: UUID) -> doctorAvailabilityResponse:
    doc = db.query(DoctorAvailability).filter(DoctorAvailability.doctor_id == doctor_id).all()
    if not doc:
        raise HTTPException(status_code=404, detail="doctor id not found")
    return [doctorAvailabilityResponse.model_validate(s) for s in doc][0]

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
    
    return doctorAvailabilityResponse.model_validate(doctor)

def delete_Doctor_Availability(db : Session, doc_id: UUID, Scheduling_id: UUID) -> dict:
    user = ensure_doctor_role(current_user=doc_id, db = db)
    id = db.query(user).filter(user.id == Scheduling_id).delete()
    if not id:
        raise HTTPException(status_code=404, detail="Scheduling id Not Found") 
    db.commit()
    return {"message": "Doctor Availability deleted successfully", "facility_id": str(doc_id)}