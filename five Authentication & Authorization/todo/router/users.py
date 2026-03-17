from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from models import Users
from database import SessionLocal
from typing import Annotated
from dependencies import user_dependence, db_dependence
from .auth import hash_password

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

# get user info
@router.get('/', status_code=status.HTTP_200_OK)
async def get_user_info(user: user_dependence, db: db_dependence):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    return db.query(Users).filter(Users.id == user.get('id')).first()

# change password
class PasswordChange(BaseModel):
    password: str

@router.put('/change-password', status_code=status.HTTP_200_OK)
async def change_password(user: user_dependence, db: db_dependence, payload: PasswordChange):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    current_user = db.query(Users).filter(Users.id == user.get('id')).first()
    if current_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    current_user.hashed_password = hash_password(payload.password)
    db.add(current_user)
    db.commit()

    return {"message": "Password updated successfully"}
