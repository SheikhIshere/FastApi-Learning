from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.crud.user import create_email_log
from app.schemas.user import Email, EmailCreate
from app.core.security import get_current_active_user
from app.core.email import smtp_service
from app.models.user import User as UserModel

router = APIRouter()


@router.post("/send", response_model=Email)
async def send_email(
    email: EmailCreate,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Create email log entry
    db_email = create_email_log(db=db, email=email)
    
    # Send email
    success = await smtp_service.send_email(
        to_email=email.to_email,
        subject=email.subject,
        body=email.body,
        email_id=db_email.id
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email")
    
    return db_email


@router.get("/logs", response_model=List[Email])
def get_email_logs(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    from app.models.user import EmailLog
    emails = db.query(EmailLog).offset(skip).limit(limit).all()
    return emails
