from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.crud.user import get_user_by_email, get_user_by_username
from app.schemas.user import User
from app.core.security import get_current_active_user
from app.models.user import User as UserModel

router = APIRouter()


@router.get("/me", response_model=User)
def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user


@router.get("/users", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users
