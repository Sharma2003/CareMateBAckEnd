from sqlalchemy import Column, String, ForeignKey, Date, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from database.core import Base
from entities.Users import User

class Patient(Base):
    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), ForeignKey(User.id), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(String,nullable=False)
    DOB = Column(Date,nullable=False)
    phoneNo = Column(String, nullable=False)
    bloodGroup = Column(String,nullable=False)
    maritalStatus = Column(String,nullable=False)
    emergencyContactName = Column(String)
    emergencyContactPhone = Column(String)
    user = relationship("User",backref="patientProfile")

    def __repr__(self):
        return f"<User(profileCompleted='{self.profileCompleted}', first_name = '{self.first_name}', last_name = '{self.last_name}')>"
