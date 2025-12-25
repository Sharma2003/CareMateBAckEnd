# patients/service.py
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from entities.Patients import Patient
from entities.Users import User
from patients.model import PatientDetails, PatientProfileResponse
import logging

def get_patient_profile(user_id: UUID, db : Session) -> PatientProfileResponse:
    patient = db.query(Patient).filter(Patient.id == user_id).first()
    if not patient:
        logging.warning(f"patient ID Not found: {user_id}")
        raise HTTPException(status_code=404, detail="Patient Profile Not Found")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    return PatientProfileResponse.model_validate(
        {**patient.__dict__, "email" : user.email,"userid":user.userid},
        from_attributes=True
        )


def upsert_patient_profile(user_id : UUID, data: PatientDetails, db: Session) -> PatientProfileResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logging.warning(f"patient ID Not found: {user_id}")
        raise HTTPException(status_code=404, detail="User Not Found")

    patient = db.query(Patient).filter(Patient.id == user_id).first()

    if not patient:
        patient = Patient(
            id=user_id,
            first_name=data.first_name,
            last_name=data.last_name,
            gender=data.gender,
            DOB=data.DOB,
            phoneNo=data.phoneNo,
            bloodGroup=data.bloodGroup,
            maritalStatus=data.maritalStatus,
            emergencyContactName=data.emergencyContactName,
            emergencyContactPhone=data.emergencyContactPhone,
        )
        db.add(patient)

    db.commit()
    db.refresh(patient)

    return PatientProfileResponse.model_validate(
        {**patient.__dict__, "email" : user.email,"userid":user.userid},
        from_attributes=True
        )

def update_patient_profile(user_id : UUID, db: Session, data : PatientDetails) -> PatientProfileResponse:
    get_patient_profile(user_id=user_id, db=db)
    user = db.query(User).filter(User.id == user_id).first()
    patient = db.query(Patient).filter(Patient.id == user_id).first()
    if patient:
        patient.first_name = data.first_name
        patient.last_name = data.last_name
        patient.gender = data.gender
        patient.DOB = data.DOB
        patient.phoneNo = data.phoneNo
        patient.bloodGroup = data.bloodGroup
        patient.maritalStatus = data.maritalStatus
        patient.emergencyContactName = data.emergencyContactName
        patient.emergencyContactPhone = data.emergencyContactPhone
    db.commit()
    return PatientProfileResponse.model_validate(
        {**patient.__dict__, "email" : user.email,"userid":user.userid},
        from_attributes=True
        )