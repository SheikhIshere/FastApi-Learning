from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from dependencies import user_dependence, db_dependence, get_current_user
from models import Todos, Users
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

user_dependence = Annotated[dict, Depends(get_current_user)] 

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)
hash_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def hash_password(password: str) -> str:
    # at first tried the bcrypt but it has a 72-byte limit and give me error
    # so i used argon2 instead , f udemy for old course suggestion
    # Use Argon2 - more secure than bcrypt, no 72-byte limit

    return hash_context.hash(password)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependence = Annotated[Session, Depends(get_db)]



def authenticate_user(username: str, password: str, db: db_dependence):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not hash_context.verify(password, user.hashed_password):
        return False
    return user

# 
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# Pydentic class
class UserCreate(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str


# Token creation class
class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependence, user: UserCreate):
    # 1. We create the object (this is fine)
    new_user = Users(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hash_password(user.password),
        role=user.role,
        is_active=True, 
        phone_number=user.phone_number
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}
    



@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependence):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}

# change phone number
@router.patch('/change/phone-number/', status_code=status.HTTP_200_OK)
async def change_phone_number(user:user_dependence, db: db_dependence, phone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    try: 
        user_model = db.query(Users).filter(Users.id == user.get('id')).first()
        if not user_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        
        user_model.phone_number = phone_number
        db.commit()
        return {"message": "Phone number updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{e}')



