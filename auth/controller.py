import sys,os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Annotated
from fastapi import APIRouter, Depends, Request
from starlette import status
from auth.model import Token, RegiserUserRequest
from auth.service import *
from fastapi.security import OAuth2PasswordRequestForm
from database.core import DbSession
from rate_limiter import limiter
 
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/register",status_code=status.HTTP_201_CREATED)
@limiter.limit("5/hour")
async def register_user(request: Request, db: DbSession, register_user_request:RegiserUserRequest):
    registered_user(db, register_user_request)

@router.post("/token",response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession):
    return login_for_access_token(form_data,db)