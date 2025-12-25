import sys,os 
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

    # class Config:
    #     orm_mode = True

