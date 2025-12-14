import sys,os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserResponse(BaseModel):
    id : UUID
    userid : str
    email : EmailStr
    role : str
    password_hash : str
    
    class Config:
        orm_mode = True


class PasswordChange(BaseModel):
    current_password : str
    new_password : str
    new_password_confirm : str

