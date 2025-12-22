from sqlalchemy import Column, ForeignKey, String, DATE, Time, Integer, SmallInteger, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from entities.Users import User
from entities.Doctor import Doctor
from database.core import Base

from entities.FacilityMaster import Facility


class DoctorAvailability(Base):
    __tablename__ = "doctor_availability"
    
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    facility_id = Column(UUID(as_uuid=True), ForeignKey(Facility.id))
    doctor_id = Column(UUID(as_uuid=True), ForeignKey(Doctor.id))
    day_of_week  = Column(SmallInteger,nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time,nullable=False)
    slot_duration_minutes = Column(Integer, default=5)
    is_active = Column(Boolean)