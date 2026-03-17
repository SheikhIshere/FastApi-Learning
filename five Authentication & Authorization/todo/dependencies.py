from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from jose import JWTError, jwt
from models import Users

SECRET_KEY = "93e09eafababf98903ca94bfd959181d467be16f366487bbff0de14a187f7a27"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')
        if username is None or user_id is None:
                raise HTTPException(
                        status_code=401,
                        detail="Could not validate credentials.",
                        headers={"WWW-Authenticate": "Bearer"},
                )
        return {'username': username, 'id': user_id, 'role': role}
    except JWTError:
        raise HTTPException(
                status_code=401,
                detail="Could not validate credentials.",
                headers={"WWW-Authenticate": "Bearer"},
        )

db_dependence = Annotated[Session, Depends(get_db)]
user_dependence = Annotated[dict, Depends(get_current_user)]
