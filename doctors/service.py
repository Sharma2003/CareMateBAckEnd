from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException
import logging
from entities.Doctor import Doctor
from entities.Users import User
from doctors.model import DoctorDetails, DoctorProfileResponse

def get_doctor_profile(user_id : UUID, db: Session) -> DoctorProfileResponse:
    doctor = db.query(Doctor).filter(Doctor.id == user_id).first()
    if not doctor:
        logging.warning(f"Doctor Profile Not Found ID: {user_id}")
        raise HTTPException(status_code=404, detail="Doctor profile not fuound")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return DoctorProfileResponse(
        id = doctor.id,
        email = user.email,
        userid = user.userid,
        profile_completed = True,
        first_name = doctor.first_name,
        last_name = doctor.last_name,
        gender = doctor.gender,
        DOB = doctor.DOB,
        phoneNo = doctor.phoneNo,
        YOE = doctor.YOE
    )


def upsert_doctor_profile(user_id : UUID, data : DoctorDetails, db : Session) -> DoctorProfileResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logging.warning(f"Doctor ID Not Found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    doctor = db.query(Doctor).filter(Doctor.id == user_id).first()

    if not doctor:
        doctor = Doctor(
            id = user_id,
            first_name = data.first_name,
            last_name = data.last_name,
            gender = data.gender,
            DOB = data.DOB,
            phoneNo = data.phoneNo,
            YOE = data.YOE
        )

        db.add(doctor)

    db.commit()
    db.refresh(doctor)

    return DoctorProfileResponse(
        id = doctor.id,
        email = user.email,
        userid = user.userid,
        profile_completed = True,
        first_name = doctor.first_name,
        last_name = doctor.last_name,
        gender = doctor.gender,
        DOB = doctor.DOB,
        phoneNo = doctor.phoneNo,
        YOE = doctor.YOE
    )


def update_doctor_profile(user_id : UUID, data : DoctorDetails, db : Session) -> DoctorProfileResponse:
    get_doctor_profile(user_id=user_id, db=db)
    doctor = db.query(Doctor).filter(Doctor.id == user_id).first()
    user = db.query(User).filter(User.id == user_id).first()
    if not user and not doctor:
        logging.warning(f"Doctor ID Not Found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    if doctor:
        doctor.first_name = data.first_name
        doctor.last_name = data.last_name
        doctor.gender = data.gender
        doctor.DOB = data.DOB
        doctor.phoneNo = data.phoneNo
        doctor.YOE = data.YOE
    db.commit()
    return DoctorProfileResponse(
        id = doctor.id,
        email = user.email,
        userid = user.userid,
        profile_completed = True,
        first_name = doctor.first_name,
        last_name = doctor.last_name,
        gender = doctor.gender,
        DOB = doctor.DOB,
        phoneNo = doctor.phoneNo,
        YOE = doctor.YOE
    )