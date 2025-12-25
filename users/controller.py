from fastapi import APIRouter, status
from users.model import *
from auth.service import *
from users.service import *
from database.core import DbSession
 
router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.get("/me",response_model=UserResponse)
def get_me(current_user: CurrentUser, db: DbSession):
    return get_user_by_id(current_user.get_uuid(),db)


@router.put("/change-password")
def change_password(db:DbSession, password_change:PasswordChange, current_user:CurrentUser):
    return changePassword(db=db,password_change=password_change,user_id=current_user.user_id)