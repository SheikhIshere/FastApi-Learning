import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings
from app.db.database import SessionLocal
from app.crud.user import update_email_status


class SMTPService:
    def __init__(self):
        self.host = settings.smtp_host
        self.port = settings.smtp_port
        self.username = settings.smtp_username
        self.password = settings.smtp_password
        self.use_tls = settings.smtp_use_tls
    
    async def send_email(self, to_email: str, subject: str, body: str, email_id: Optional[int] = None) -> bool:
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.username or "noreply@example.com"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(body, 'plain'))
            
            # Create SMTP session
            server = smtplib.SMTP(self.host, self.port)
            
            if self.use_tls:
                server.starttls()
            
            if self.username and self.password:
                server.login(self.username, self.password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(msg['From'], to_email, text)
            server.quit()
            
            # Update email status in database
            if email_id:
                db = SessionLocal()
                try:
                    update_email_status(db, email_id, "sent")
                finally:
                    db.close()
            
            return True
            
        except Exception as e:
            # Update email status with error
            if email_id:
                db = SessionLocal()
                try:
                    update_email_status(db, email_id, "failed", str(e))
                finally:
                    db.close()
            
            print(f"Failed to send email: {e}")
            return False


smtp_service = SMTPService()
