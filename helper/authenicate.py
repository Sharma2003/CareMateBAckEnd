from auth.service import CurrentUser
from fastapi import HTTPException

def authorize_user_access(current_user:str, user_name:str):
    if current_user != user_name:
        raise HTTPException(status_code=403, detail="You are not authorized to access this user")
    