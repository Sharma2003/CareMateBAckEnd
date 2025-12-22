from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

# from entities.Users import User
from entities.FacilityMaster import Facility
from facilites.model import FacilityResponse, FacilitiesDetails
import logging

def create_doctor_facility(db : Session, payload : FacilitiesDetails, doctor_id:UUID) -> FacilityResponse:
    facility = Facility(
        doctor_id = doctor_id,
        facilityName = payload.facilityName,
        facilityType = payload.facilityType,
        facilityAddress = payload.facilityAddress,
        city = payload.city,
        state = payload.state,
        postalCode = payload.postalCode
    )
    db.add(facility)
    db.commit()
    db.refresh(facility)

    return Facility(
        id = facility.id,
        doctor_id = facility.doctor_id,
        facilityName = facility.facilityName,
        facilityType = facility.facilityType,
        facilityAddress = facility.facilityAddress,
        city = facility.city,
        state = facility.state,
        postalCode = facility.postalCode
    )

def get_facility(db :Session, current_user : UUID):
    facility = db.query(Facility).filter(Facility.doctor_id == current_user).all()
    if not facility:
        logging.warning(f"Facility Not Found: {current_user}")
        raise HTTPException(status_code=404, detail="Facility not found")
    return facility


def update_facility(db: Session, facility_id : UUID, payload : FacilitiesDetails) -> FacilityResponse:
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        logging.warning(f"Facility Not Found: {facility_id}")
        raise HTTPException(status_code=404, detail="For updating the data you need to first create one")
    
    facility.facilityName = payload.facilityName
    facility.facilityType = payload.facilityType
    facility.facilityAddress = payload.facilityAddress
    facility.city = payload.city
    facility.postalCode = payload.postalCode
    db.commit()
    return facility

def delete_facility(db : Session , facility_id : UUID) -> FacilityResponse:
    facility = db.query(Facility).filter(Facility.id == facility_id).delete()
    if not facility:
        logging.warning(f"Facility Not Found: {facility_id}")
        raise HTTPException(status_code=404, detail="Facility Not Found") 
    db.commit()
    return facility 