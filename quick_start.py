#!/usr/bin/env python3
"""
Quick Start Script for MarketPro Backend
Gets the backend running quickly with current configuration
"""
import os
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'sqlalchemy', 'pydantic', 
        'python-jose', 'passlib', 'psycopg2'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please run: python install_dependencies.py")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_database():
    """Check if database is accessible"""
    print("\n🗄️  Checking database connection...")
    
    try:
        from app.database.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your PostgreSQL setup and .env configuration")
        return False

def check_email_config():
    """Check email configuration"""
    print("\n📧 Checking email configuration...")
    
    from app.core.config import settings
    
    if settings.smtp_user and settings.smtp_password:
        print(f"✅ Email configured: {settings.smtp_user}")
        return True
    else:
        print("⚠️  Email not configured (optional)")
        return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("\n📝 Creating .env file...")
        try:
            subprocess.run(['cp', 'env.example', '.env'], check=True)
            print("✅ .env file created from template")
            print("⚠️  Please update .env with your actual credentials")
            return False
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file exists")
        return True

def initialize_database():
    """Initialize database with sample data"""
    print("\n🗄️  Initializing database...")
    
    try:
        from app.database.database import engine
        from app.models import user, course, enrollment, content
        
        # Create tables
        user.Base.metadata.create_all(bind=engine)
        course.Base.metadata.create_all(bind=engine)
        enrollment.Base.metadata.create_all(bind=engine)
        content.Base.metadata.create_all(bind=engine)
        
        print("✅ Database tables created")
        
        # Check if sample data exists
        from sqlalchemy.orm import Session
        from app.models.user import User
        
        db = Session(engine)
        admin_count = db.query(User).filter(User.role.value == "admin").count()
        db.close()
        
        if admin_count == 0:
            print("📊 Creating sample data...")
            subprocess.run([sys.executable, 'init_db.py'], check=True)
            print("✅ Sample data created")
        else:
            print("✅ Sample data already exists")
        
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting FastAPI server...")
    print("Server will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'app.main:app', 
            '--host', '0.0.0.0', 
            '--port', '8000', 
            '--reload'
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    print("🚀 MarketPro Backend - Quick Start")
    print("="*40)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        return
    
    # Step 2: Check/create .env file
    env_ready = create_env_file()
    
    # Step 3: Check database
    if not check_database():
        return
    
    # Step 4: Check email config
    check_email_config()
    
    # Step 5: Initialize database
    if not initialize_database():
        return
    
    # Step 6: Start server
    start_server()

if __name__ == "__main__":
    main()
