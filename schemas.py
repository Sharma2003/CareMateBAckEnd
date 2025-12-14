from pydantic import BaseModel, EmailStr
from datetime import date


class UserSignUp(BaseModel):
    UserID : str
    FirstName : str
    LastName : str
    Gender : str
    DOB : date
    MobileNO : str
    EmailID : EmailStr
    YOE : int
    password : str

class UserLogIn(BaseModel):
    UserID : str
    EmailID : EmailStr
    password : str

# class profile(BaseModel):
#     UserID : str
#     FirstName : str
#     LastName : str
#     Gender : str
#     DOB : date
#     MobileNO : str
#     EmailID : EmailStr
#     YOE : int