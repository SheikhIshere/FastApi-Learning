from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session, dependency
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
 
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)
hash_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


SECRET_KEY = "93e09eafababf98903ca94bfd959181d467be16f366487bbff0de14a187f7a27"  # TODO: Use environment variable in production
ALGORITHM = "HS256"



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
def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
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
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}
    

# @router.get("/", status_code=status.HTTP_200_OK)
# def read_root():
#     return {"user": "authenticated"}


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )
        
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user",
        )


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependence):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}
