from sqlalchemy.orm import Session
from app.models.user import User, EmailLog
from app.schemas.user import UserCreate, EmailCreate
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_email_log(db: Session, email: EmailCreate):
    db_email = EmailLog(**email.dict())
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email


def update_email_status(db: Session, email_id: int, status: str, error_message: Optional[str] = None):
    db_email = db.query(EmailLog).filter(EmailLog.id == email_id).first()
    if db_email:
        db_email.status = status
        db_email.error_message = error_message
        if status == "sent":
            from datetime import datetime
            db_email.sent_at = datetime.utcnow()
        db.commit()
        db.refresh(db_email)
    return db_email
