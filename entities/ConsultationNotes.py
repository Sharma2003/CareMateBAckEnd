import uuid
from sqlalchemy import Column, String , Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database.core import Base

class ConsultationNotes(Base):
    __tablename__ ='consultation_notes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('consultation_session.id'))
    # doctor_id = Column(UUID(as_uuid=True), ForeignKey("consultation_session.doctor_id"))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id",ondelete="CASCADE"))

    note_text = Column(Text)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    session = relationship("ConsultationSession", back_populates="notes")