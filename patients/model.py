import sys,os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date

class PatientDetails(BaseModel):
    first_name : str
    last_name : str
    gender : str
    DOB : date
    phoneNo : str
    bloodGroup : str
    maritalStatus : str
    emergencyContactName : str
    emergencyContactPhone : str


class PatientProfileResponse(PatientDetails):
    id : UUID
    email : EmailStr
    userid : str
    profile_compeleted : bool

    class Config:
        orm_mode = True

