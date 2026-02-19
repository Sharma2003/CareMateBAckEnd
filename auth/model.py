from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, SecretStr
from functools import partial
from typing import Literal, Annotated
from datetime import datetime, UTC

class RegiserUserRequest(BaseModel):
    userid : Annotated[str, Field(min_length=5,max_length=20)]
    email : EmailStr
    role : Literal["patient","doctor"] = None
    password : SecretStr
    # created_at = Annotated[datetime,Field(default_factory=partial(datetime.now,tz=UTC))]

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    user_name : str | None = None
    user_id : str | None = None
    def get_uuid(self) -> UUID | None:
        if self.user_id:
            return UUID(self.user_id)
        return None
    
    # def get_username(self) -> str | None:
    #     if self.user_name:
    #         return str(self.user_name)
    #     return None