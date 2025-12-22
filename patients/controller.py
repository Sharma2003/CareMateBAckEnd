from fastapi import APIRouter, Depends, HTTPException
from database.core import DbSession, Base, engine
from auth.service import CurrentUser
from entities.Users import User
from entities.Patients import Patient
from patients.model import PatientDetails, PatientProfileResponse
from patients.service import get_patient_profile, upsert_patient_profile, update_patient_profile
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)

def ensure_patient_role(current_user : CurrentUser, db : Session):
    user=db.query(User).filter(User.id == current_user.get_uuid()).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    if user.role != "patient":
        raise HTTPException(status_code=403,detail="only patient can access this resource")
    
    return user

@router.get("/profile",response_model=PatientProfileResponse)
def get_my_profile(current_user: CurrentUser, db : DbSession):
    ensure_patient_role(current_user=current_user, db=db)
    return get_patient_profile(current_user.get_uuid(), db)

@router.post("/profile",response_model=PatientProfileResponse)
def create_profile(
    payload: PatientDetails,
    current_user : CurrentUser,
    db : DbSession
):
    ensure_patient_role(current_user=current_user,db=db)
    return upsert_patient_profile(user_id=current_user.get_uuid(), data=payload, db=db)

@router.put("/profile",response_model=PatientProfileResponse)
def update_profile(current_user: CurrentUser, db: DbSession, payload : PatientDetails):
    ensure_patient_role(current_user=current_user, db=db)
    return update_patient_profile(user_id=current_user.get_uuid(), db=db, data=payload)