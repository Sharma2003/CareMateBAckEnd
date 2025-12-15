from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID
from database.core import DbSession
from facilites.service import create_doctor_facility, get_facility, update_facility, delete_facility
from facilites.model import FacilitiesDetails, FacilityResponse
from auth.service import CurrentUser
from entities.Users import User
from entities.FacilityMaster import Facility

router = APIRouter(
    prefix="/facilities",
    tags=["facilities"]
)

def ensure_doctor_role(current_user : CurrentUser, db : Session):
    user = db.query(User).filter(User.id == current_user.get_uuid()).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.role != 'doctor'.lower():
        raise HTTPException(status_code=403, detail="only doctors can access this resouces")
    
    return user

@router.post("/",response_model=FacilityResponse)
def create(current_user : CurrentUser, payload : FacilitiesDetails, db : DbSession):
    ensure_doctor_role(current_user=current_user, db=db)
    return create_doctor_facility(db=db, payload=payload)

@router.get("/get_facility/{facility_id}",response_model=FacilityResponse)
def get_facility_by_id(facility_id : UUID, db : DbSession):
    return get_facility(facility_id=facility_id, db=db)

@router.put("/update_facility/{facility_id}",response_model=FacilityResponse)
def update(facility_id : UUID, db : DbSession, payload : FacilitiesDetails):
    return update_facility(facility_id=facility_id, db=db, payload=payload)

@router.delete("/delete_facility/{facility_id}")
def delete(facility_id : UUID, db : DbSession):
    return delete_facility(db=db, facility_id=facility_id)