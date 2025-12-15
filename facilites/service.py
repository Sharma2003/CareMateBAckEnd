import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

# from entities.Users import User
from entities.FacilityMaster import Facility
from facilites.model import FacilityResponse, FacilitiesDetails

def create_doctor_facility(db : Session, payload : FacilitiesDetails) -> Facility:
    facility = Facility(
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

    return facility

def get_facility(db :Session, facility_id : UUID) -> Facility:
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    return facility


def update_facility(db: Session, facility_id : UUID, payload : FacilitiesDetails) -> Facility:
    facility = db.query(Facility).filter(Facility.id == facility_id).first()
    if not facility:
        raise HTTPException(status_code=404, detail="For updating the data you need to first create one")
    
    facility.facilityName = payload.facilityName
    facility.facilityType = payload.facilityType
    facility.facilityAddress = payload.facilityAddress
    facility.city = payload.city
    facility.postalCode = payload.postalCode
    db.commit()
    return facility

def delete_facility(db : Session , facility_id : UUID) -> Facility:
    facility = db.query(Facility).filter(Facility.id == facility_id).delete()
    if not facility:
        raise HTTPException(status_code=404, detail="Facility Not Found") 
    db.commit()
    return facility 