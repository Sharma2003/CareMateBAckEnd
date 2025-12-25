from sqlalchemy import Column, DateTime, UUID, ForeignKey, String, UniqueConstraint, TIME
from sqlalchemy.sql import func
from database.core import Base
from entities.Patients import Patient
from entities.Doctor import Doctor
from entities.FacilityMaster import Facility
import uuid
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey(Doctor.id,  ondelete="CASCADE"), nullable=False)
    patient_id = Column(UUID(as_uuid=True), ForeignKey(Patient.id,  ondelete="CASCADE"), nullable=False)
    facility_id = Column(UUID(as_uuid=True), ForeignKey(Facility.id,  ondelete="CASCADE"), nullable=False)
    start_ts = Column(TIME, nullable=False)
    end_ts = Column(TIME,nullable=False)
    status = Column(String(20), nullable=False, default="booked")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "start_ts",
            name="uq_doctor_start_time"
        ),
    )
