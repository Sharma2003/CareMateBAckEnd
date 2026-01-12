from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import logging

from entities.Booking import Booking
from entities.DoctorFacility import DoctorAvailability
from booking.model import bookingSlots, bookingSlotsResponse

# from helper.ensure import ensure_patient_role 

def bookAppointment(db : Session, currentUser : UUID, doctor_id : UUID, facility_id : UUID, payload : Booking) -> bookingSlotsResponse:
    availability = db.query(DoctorAvailability).filter(DoctorAvailability.doctor_id == doctor_id and DoctorAvailability.facility_id == facility_id).all()
    if not availability:
        logging.warning(f"User not found with ID: {doctor_id}. {doctor_id}")
        raise HTTPException(status_code=404, detail="Faility Not Available")
    
    booking_appointment = Booking(
        facility_id = facility_id,
        doctor_id = doctor_id,
        patient_id = currentUser,
        start_ts = payload.start_ts,
        end_ts = payload.end_ts,
        status = payload.status
    )

    db.add(booking_appointment)
    db.commit()
    db.refresh(booking_appointment) 
    return bookingSlotsResponse.model_validate(booking_appointment,from_attributes=True)


def get_patient_appointments(db:Session, patient_id : UUID):
    patient = db.query(Booking).filter(Booking.patient_id == patient_id).order_by(Booking.start_ts).all()
    return patient

def get_doctor_appointments(db:Session, doctor_id : UUID):
    doctor = db.query(Booking).filter(Booking.doctor_id == doctor_id).order_by(Booking.start_ts).all()
    return doctor
