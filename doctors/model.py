from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import date
from typing import Annotated, Optional, Literal

class DoctorDetails(BaseModel):
    first_name : Annotated[str,Field(min_length=1,max_length=20)]
    last_name : Annotated[str,Field(min_length=1, max_length=20)]
    gender : Optional[Literal['male','female','others']]
    DOB : date
    phoneNo : str
    YOE : int

class DoctorProfileResponse(DoctorDetails):
    id : UUID
    email : EmailStr
    userid : str

