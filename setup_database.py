#!/usr/bin/env python3
"""
Database and Email Setup Script for MarketPro Backend
This script helps set up PostgreSQL database and provides Gmail SMTP instructions
"""
import os
import subprocess
import sys
from pathlib import Path

def check_postgresql():
    """Check if PostgreSQL is installed and running"""
    try:
        # Check if psql is available
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PostgreSQL is installed")
            print(f"   Version: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL is not installed or not in PATH")
        return False

def create_database():
    """Create the wealth database"""
    try:
        # Try to create database
        result = subprocess.run([
            'psql', '-U', 'postgres', '-h', 'localhost', 
            '-c', 'CREATE DATABASE wealth;'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database 'wealth' created successfully")
            return True
        elif "already exists" in result.stderr:
            print("✅ Database 'wealth' already exists")
            return True
        else:
            print(f"❌ Error creating database: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def setup_environment():
    """Set up environment variables"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        subprocess.run(['cp', 'env.example', '.env'])
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")

def print_gmail_setup_instructions():
    """Print Gmail SMTP setup instructions"""
    print("\n" + "="*60)
    print("📧 GMAIL SMTP SETUP INSTRUCTIONS")
    print("="*60)
    print("""
To use Gmail for sending emails, follow these steps:

1. Enable 2-Factor Authentication on your Gmail account:
   - Go to Google Account settings
   - Security → 2-Step Verification → Turn it on

2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and "Other (Custom name)"
   - Name it "MarketPro Backend"
   - Copy the generated 16-character password

3. Update your .env file:
   - Set SMTP_USER=your-gmail@gmail.com
   - Set SMTP_PASSWORD=your-16-character-app-password

4. Test the email configuration by running:
   python -c "
from app.utils.email import send_email
send_email('test@example.com', 'Test', 'This is a test email')
   "
""")

def print_postgresql_setup_instructions():
    """Print PostgreSQL setup instructions"""
    print("\n" + "="*60)
    print("🗄️  POSTGRESQL SETUP INSTRUCTIONS")
    print("="*60)
    print("""
If PostgreSQL is not installed or you need to set it up:

WINDOWS:
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Install with default settings
3. Remember the password you set for 'postgres' user
4. Update .env file with your password

MAC:
1. Install using Homebrew: brew install postgresql
2. Start service: brew services start postgresql
3. Create user: createuser -s postgres

LINUX (Ubuntu/Debian):
1. Install: sudo apt-get install postgresql postgresql-contrib
2. Start service: sudo systemctl start postgresql
3. Switch to postgres user: sudo -u postgres psql
4. Set password: ALTER USER postgres PASSWORD 'your_password';

After installation:
1. Update .env file with your PostgreSQL password
2. Run this script again to create the database
""")

def main():
    print("🚀 MarketPro Backend Setup Script")
    print("="*40)
    
    # Check PostgreSQL
    if not check_postgresql():
        print_postgresql_setup_instructions()
        return
    
    # Create database
    if not create_database():
        print("\n❌ Failed to create database. Please check PostgreSQL setup.")
        return
    
    # Setup environment
    setup_environment()
    
    # Print Gmail instructions
    print_gmail_setup_instructions()
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("""
Next steps:
1. Update your .env file with your actual credentials
2. Run: python init_db.py (to create sample data)
3. Run: python start.py (to start the server)
4. Visit: http://localhost:8000/docs (for API documentation)

Sample .env configuration:
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/marketpro_db
SMTP_USER=your-gmail@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SECRET_KEY=your-long-random-secret-key
""")

if __name__ == "__main__":
    main()
