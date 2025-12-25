from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserResponse(BaseModel):
    id : UUID
    userid : str
    email : EmailStr
    role : str

class UserPasswordResponse(UserResponse):
    password_hash : str

class PasswordChange(BaseModel):
    current_password : str
    new_password : str
    new_password_confirm : str

