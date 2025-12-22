from uuid import UUID
from pydantic import BaseModel, EmailStr

class RegiserUserRequest(BaseModel):
    userid : str
    email : EmailStr
    role : str
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    user_id : str | None = None
    def get_uuid(self) -> UUID | None:
        if self.user_id:
            return UUID(self.user_id)
        return None