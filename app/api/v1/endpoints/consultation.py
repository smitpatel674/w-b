from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from app.api.deps import get_db
from app.models.consultation import ConsultationSchedule

router = APIRouter()

class ConsultationRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    date: str
    time: str
    message: Optional[str] = None

# Gmail SMTP configuration from environment
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "smitpatidar6704@gmail.com")
GMAIL_USER = os.getenv("SMTP_USER", "smitpatidar6704@gmail.com")
GMAIL_PASSWORD = os.getenv("SMTP_PASSWORD", "avec awrj wxuw uhcu")

def send_email(to_email: str, subject: str, body: str, is_html: bool = False):
    """Send email using Gmail SMTP"""
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        if is_html:
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(body, 'plain'))
        
        # Gmail SMTP connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(GMAIL_USER, to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def format_consultation_date_time(date_str: str, time_str: str) -> str:
    """Format date and time for display"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%A, %B %d, %Y")
        
        # Convert 24-hour time to 12-hour format
        time_obj = datetime.strptime(time_str, "%H:%M")
        formatted_time = time_obj.strftime("%I:%M %p")
        
        return f"{formatted_date} at {formatted_time}"
    except:
        return f"{date_str} at {time_str}"

@router.post("/schedule-consultation")
async def schedule_consultation(
    request: ConsultationRequest,
    db: Session = Depends(get_db)
):
    try:
        # Save to database
        consultation = ConsultationSchedule(
            name=request.name,
            email=request.email,
            phone=request.phone,
            preferred_date=request.date,
            preferred_time=request.time,
            message=request.message,
            status="scheduled",
            created_at=datetime.utcnow()
        )
        
        db.add(consultation)
        db.commit()
        db.refresh(consultation)
        
        # Format date and time for emails
        consultation_datetime = format_consultation_date_time(request.date, request.time)
        
        # Send confirmation email to user
        user_subject = "Consultation Scheduled - Wealth Genius"
        user_body = f"""
Dear {request.name},

Thank you for scheduling a free consultation with Wealth Genius!

Your consultation details:
📅 Date & Time: {consultation_datetime}
📧 Email: {request.email}
📱 Phone: {request.phone}

What to expect during your consultation:
• 30-minute one-on-one session with our trading expert
• Personalized trading strategy discussion
• Course recommendations based on your goals
• Q&A session to address your concerns

Our expert will contact you 5 minutes before the scheduled time. Please ensure you're available at the provided phone number.

If you need to reschedule or have any questions, please contact us at:
📧 Email: smitpatidar6704@gmail.com
📱 Phone: +91 96245 18383

We look forward to helping you achieve your trading goals!

Best regards,
The Wealth Genius Team

---
Wealth Genius - Your Gateway to Financial Success
409/ Golden Square, Near, Kalyan Chowk, Nikol
Ahmedabad, Gujarat - 382350
"""
        
        # Send notification email to admin
        admin_subject = f"New Consultation Scheduled - {request.name}"
        admin_body = f"""
New consultation scheduled on Wealth Genius platform:

Client Details:
👤 Name: {request.name}
📧 Email: {request.email}
📱 Phone: {request.phone}
📅 Preferred Date & Time: {consultation_datetime}

Additional Message:
{request.message if request.message else 'No additional message provided'}

Consultation ID: {consultation.id}
Scheduled At: {consultation.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}

Please ensure to contact the client at the scheduled time.

---
Wealth Genius Admin Panel
"""
        
        # Send emails
        user_email_sent = send_email(request.email, user_subject, user_body)
        admin_email_sent = send_email(ADMIN_EMAIL, admin_subject, admin_body)
        
        if not user_email_sent:
            print("Warning: Failed to send confirmation email to user")
        if not admin_email_sent:
            print("Warning: Failed to send notification email to admin")
        
        return {
            "message": "Consultation scheduled successfully!",
            "consultation_id": consultation.id,
            "scheduled_datetime": consultation_datetime,
            "email_sent": user_email_sent
        }
        
    except Exception as e:
        db.rollback()
        print(f"Error scheduling consultation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to schedule consultation")