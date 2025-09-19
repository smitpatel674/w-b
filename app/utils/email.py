import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


def send_email(to_email: str, subject: str, body: str, html_body: str = None):
    """Send email using SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.smtp_user
        msg['To'] = to_email

        # Attach plain text
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)

        # Attach HTML if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)

        # Send email
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_contact_notification_email(inquiry):
    """Send notification email for new contact inquiry"""
    subject = f"New Contact Inquiry: {inquiry.subject}"
    body = f"""
    New contact inquiry received:
    
    Name: {inquiry.name}
    Email: {inquiry.email}
    Phone: {inquiry.phone or 'Not provided'}
    Subject: {inquiry.subject}
    Message: {inquiry.message}
    Course Interest: {inquiry.course_interest or 'Not specified'}
    
    Received at: {inquiry.created_at}
    """
    
    # Send to admin email (you can configure this in settings)
    admin_email = "admin@marketpro.com"  # Configure this
    return send_email(admin_email, subject, body)


def send_welcome_email(user):
    """Send welcome email to new user"""
    subject = "Welcome to Wealth Genius Trading Education Platform"
    body = f"""
    Welcome to Wealth Genius, {user.full_name}!
    
    Thank you for joining our trading education platform. We're excited to help you on your journey to becoming a successful trader.
    
    Your account details:
    - Username: {user.username}
    - Email: {user.email}
    
    Get started by exploring our courses and joining our community.
    
    Best regards,
    The Wealth Genius Team
    """
    
    return send_email(user.email, subject, body)
