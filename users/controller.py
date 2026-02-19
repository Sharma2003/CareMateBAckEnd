from fastapi import APIRouter, status
from users.model import *
from auth.service import *
from users.service import *
from database.core import DbSession
from helper.authenicate import authorize_user_access
 
router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.get("/{user_name}")
def get_me(user_name:str,current_user: CurrentUser, db: DbSession):
    authorize_user_access(current_user.user_name,user_name)
    print(current_user.user_name)
    return get_user_by_id(current_user.get_uuid(),db)


@router.put("/change-password")
def change_password(db:DbSession, password_change:PasswordChange, current_user:CurrentUser):
    return changePassword(db=db,password_change=password_change,user_id=current_user.user_id)