#!/usr/bin/env python3
"""
Email Test Script for MarketPro Backend
Tests Gmail SMTP configuration
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_configuration():
    """Test the email configuration"""
    print("📧 Testing Email Configuration")
    print("="*40)
    
    # Check environment variables
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = os.getenv('SMTP_PORT')
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    print(f"SMTP Host: {smtp_host}")
    print(f"SMTP Port: {smtp_port}")
    print(f"SMTP User: {smtp_user}")
    print(f"SMTP Password: {'*' * len(smtp_password) if smtp_password else 'Not set'}")
    
    if not all([smtp_host, smtp_port, smtp_user, smtp_password]):
        print("\n❌ Missing email configuration in .env file")
        print("Please set the following variables:")
        print("- SMTP_HOST=smtp.gmail.com")
        print("- SMTP_PORT=587")
        print("- SMTP_USER=your-gmail@gmail.com")
        print("- SMTP_PASSWORD=your-gmail-app-password")
        return False
    
    # Test email sending
    try:
        from app.utils.email import send_email
        
        test_email = input("\nEnter test email address (or press Enter to skip): ").strip()
        if not test_email:
            print("Skipping email test")
            return True
        
        print(f"\nSending test email to {test_email}...")
        
        success = send_email(
            to_email=test_email,
            subject="MarketPro Backend - Email Test",
            body="This is a test email from MarketPro Backend. If you receive this, your Gmail SMTP configuration is working correctly!"
        )
        
        if success:
            print("✅ Test email sent successfully!")
            return True
        else:
            print("❌ Failed to send test email")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the Backend directory")
        return False
    except Exception as e:
        print(f"❌ Error testing email: {e}")
        return False

def main():
    print("🚀 MarketPro Backend - Email Test")
    print("="*40)
    
    if test_email_configuration():
        print("\n✅ Email configuration is working correctly!")
    else:
        print("\n❌ Email configuration needs to be fixed")
        print("\nCommon issues:")
        print("1. Gmail 2-Factor Authentication not enabled")
        print("2. App password not generated correctly")
        print("3. Incorrect email/password in .env file")
        print("4. Gmail account security settings blocking access")

if __name__ == "__main__":
    main()
