import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date

class DoctorDetails(BaseModel):
    first_name : str
    last_name : str
    gender : str
    DOB : date
    phoneNo : str
    YOE : int

class DoctorProfileResponse(DoctorDetails):
    id : UUID
    email : EmailStr
    userid : str
    profile_completed : bool

    # class Config:
    #     orm_mode = True

