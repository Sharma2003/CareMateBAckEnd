from fastapi import APIRouter
from auth.service import CurrentUser
from database.core import DbSession
from entities.Doctor import Doctor
from entities.Patients import Patient
from entities.FacilityMaster import Facility
from helper.ensure import ensure_patient_role
from booking.model import bookingSlotsResponse,bookingSlots
from booking.service import bookAppointment
from uuid import UUID

router = APIRouter(
    prefix="/Booking",
    tags=["Booking"]
)

@router.post("/create", response_model=bookingSlotsResponse)
def create(db : DbSession, currentuser : CurrentUser, facility_id : UUID, doctor_id : UUID, payload:bookingSlots):
    ensure_patient_role(db=db, current_user=currentuser.get_uuid())
    return bookAppointment(db=db, currentUser=currentuser.get_uuid(), doctor_id=doctor_id, facility_id=facility_id, payload=payload)
