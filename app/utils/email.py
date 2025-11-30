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


def send_enrollment_confirmation_email(student_name: str, student_email: str, course_title: str, course_price: str, enrollment_id: int):
    """Send enrollment confirmation email to student"""
    subject = f"Enrollment Confirmation - {course_title} | Wealth Genius"
    
    # Plain text version
    body = f"""
Dear {student_name},

Thank you for enrolling in {course_title} with Wealth Genius!

Your enrollment has been successfully submitted and is currently being processed.

Enrollment Details:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Course: {course_title}
Course Fee: {course_price}
Enrollment ID: #{enrollment_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What Happens Next?
• Our team will review your enrollment request
• You will receive a call from our team within 24-48 hours
• We will guide you through the payment process
• Once payment is confirmed, you'll get access to course materials

Contact Information:
📧 Email: smitpatidar6704@gmail.com
📱 Phone: +91 96245 18383
📍 Address: 409/ Golden Square, Near, Kalyan Chowk, Nikol, Ahmedabad, Gujarat - 382350

We're excited to help you on your trading journey!

Best regards,
The Wealth Genius Team

---
Wealth Genius Trading Education Platform
Your Gateway to Financial Success
"""
    
    # HTML version
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #1e40af, #059669);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }}
        .content {{
            background: #f9fafb;
            padding: 30px;
            border: 1px solid #e5e7eb;
        }}
        .details-box {{
            background: white;
            border-left: 4px solid #3b82f6;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .detail-row {{
            padding: 10px 0;
            border-bottom: 1px solid #e5e7eb;
        }}
        .detail-row:last-child {{
            border-bottom: none;
        }}
        .detail-label {{
            font-weight: bold;
            color: #6b7280;
            display: inline-block;
            width: 150px;
        }}
        .detail-value {{
            color: #111827;
        }}
        .next-steps {{
            background: #eff6ff;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .next-steps h3 {{
            color: #1e40af;
            margin-top: 0;
        }}
        .next-steps ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .next-steps li {{
            margin: 8px 0;
        }}
        .contact-info {{
            background: #f0fdf4;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .contact-info h3 {{
            color: #059669;
            margin-top: 0;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #6b7280;
            font-size: 12px;
            border-top: 1px solid #e5e7eb;
        }}
        .button {{
            display: inline-block;
            background: #3b82f6;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 Enrollment Confirmation</h1>
        <p>Wealth Genius Trading Education Platform</p>
    </div>
    
    <div class="content">
        <p>Dear <strong>{student_name}</strong>,</p>
        
        <p>Thank you for enrolling in <strong>{course_title}</strong> with Wealth Genius!</p>
        
        <p>Your enrollment has been successfully submitted and is currently being processed.</p>
        
        <div class="details-box">
            <h3 style="margin-top: 0; color: #1e40af;">Enrollment Details</h3>
            <div class="detail-row">
                <span class="detail-label">Course:</span>
                <span class="detail-value">{course_title}</span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Course Fee:</span>
                <span class="detail-value"><strong>{course_price}</strong></span>
            </div>
            <div class="detail-row">
                <span class="detail-label">Enrollment ID:</span>
                <span class="detail-value">#{enrollment_id}</span>
            </div>
        </div>
        
        <div class="next-steps">
            <h3>📋 What Happens Next?</h3>
            <ul>
                <li>Our team will review your enrollment request</li>
                <li>You will receive a call from our team within <strong>24-48 hours</strong></li>
                <li>We will guide you through the payment process</li>
                <li>Once payment is confirmed, you'll get access to course materials</li>
            </ul>
        </div>
        
        <div class="contact-info">
            <h3>📞 Contact Information</h3>
            <p><strong>📧 Email:</strong> smitpatidar6704@gmail.com</p>
            <p><strong>📱 Phone:</strong> +91 96245 18383</p>
            <p><strong>📍 Address:</strong> 409/ Golden Square, Near, Kalyan Chowk, Nikol, Ahmedabad, Gujarat - 382350</p>
        </div>
        
        <p>We're excited to help you on your trading journey!</p>
        
        <p>Best regards,<br>
        <strong>The Wealth Genius Team</strong></p>
    </div>
    
    <div class="footer">
        <p>Wealth Genius Trading Education Platform</p>
        <p>Your Gateway to Financial Success</p>
        <p>© 2025 Wealth Genius. All rights reserved.</p>
    </div>
</body>
</html>
"""
    
    return send_email(student_email, subject, body, html_body)