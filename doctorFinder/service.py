from fastapi import HTTPException
from sqlalchemy.orm import Session
from entities.FacilityMaster import Facility

def get_factility(db: Session):
    user = [i[0] for i in db.query(Facility.facilityName).all()]
    return user

def get_doctor(db:Session, facilityname : str):
    user =  [i[0] for i in db.query(Facility.doctor_id).filter(Facility.facilityName == facilityname).all()]
    return user


