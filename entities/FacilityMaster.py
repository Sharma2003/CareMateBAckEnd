import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import Column, String,Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

# from entities.Users import User
from entities.Doctor import Doctor
# from entities.Patients import Patient
from database.core import Base
import uuid


class Facility(Base):
    __tablename__ = "facility"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True),ForeignKey(Doctor.id))
    facilityName = Column(String,  nullable=False)
    facilityType = Column(String, nullable=False)
    facilityAddress = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postalCode = Column(Integer, nullable=False)

    # doctors = relationship(
    #         "DoctorFacility",
    #         back_populates="facility",
    #         cascade="all, delete"
    #     )

