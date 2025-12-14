import sys,os 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException
from users.model import *
from entities.Users import User
from auth.service import verify_password, get_password_hash
from database.core import *

def get_user_by_id(user_id : UUID, db : Session) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user

def changePassword(user_id: UUID, password_change: PasswordChange, db : Session) -> None:
    try:
        user = get_user_by_id(db=db, user_id=user_id)
        if not verify_password(plain_password=password_change.current_password, hashed_password=user.password_hash):
            raise HTTPException(status_code=404, detail="Incorrect password")
        if password_change.new_password != password_change.new_password_confirm:
            raise HTTPException(detail="password do not match")
        user.password_hash = get_password_hash(password_change.new_password)
        db.commit()
        return {"message":"Password Updated"}
    except Exception as e:
        raise e         
