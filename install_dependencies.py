#!/usr/bin/env python3
"""
Dependency Installation Script for MarketPro Backend
Installs dependencies step by step to avoid conflicts
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n📦 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 MarketPro Backend - Dependency Installation")
    print("="*50)
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: You're not in a virtual environment!")
        print("It's recommended to create one first:")
        print("python -m venv venv")
        print("venv\\Scripts\\activate  # Windows")
        print("source venv/bin/activate  # Mac/Linux")
        
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Upgrade pip first
    if not run_command("python -m pip install --upgrade pip", "Upgrading pip"):
        print("❌ Failed to upgrade pip. Please try manually: python -m pip install --upgrade pip")
        return
    
    # Install core dependencies first
    core_deps = [
        ("fastapi==0.104.1", "FastAPI framework"),
        ("uvicorn[standard]==0.24.0", "ASGI server"),
        ("pydantic==2.5.0", "Data validation"),
        ("pydantic-settings==2.1.0", "Settings management"),
        ("python-dotenv==1.0.0", "Environment variables"),
    ]
    
    for dep, desc in core_deps:
        if not run_command(f"pip install {dep}", f"Installing {desc}"):
            print(f"❌ Failed to install {desc}")
            return
    
    # Install database dependencies
    db_deps = [
        ("sqlalchemy==2.0.23", "SQLAlchemy ORM"),
        ("alembic==1.12.1", "Database migrations"),
        ("psycopg2-binary==2.9.9", "PostgreSQL adapter"),
    ]
    
    for dep, desc in db_deps:
        if not run_command(f"pip install {dep}", f"Installing {desc}"):
            print(f"❌ Failed to install {desc}")
            return
    
    # Install authentication dependencies
    auth_deps = [
        ("python-jose[cryptography]==3.3.0", "JWT tokens"),
        ("passlib[bcrypt]==1.7.4", "Password hashing"),
        ("python-multipart==0.0.6", "Form data parsing"),
        ("email-validator==2.1.0", "Email validation"),
    ]
    
    for dep, desc in auth_deps:
        if not run_command(f"pip install {dep}", f"Installing {desc}"):
            print(f"❌ Failed to install {desc}")
            return
    
    # Install file handling dependencies
    file_deps = [
        ("boto3==1.34.0", "AWS SDK"),
        ("pillow==10.1.0", "Image processing"),
    ]
    
    for dep, desc in file_deps:
        if not run_command(f"pip install {dep}", f"Installing {desc}"):
            print(f"❌ Failed to install {desc}")
            return
    
    # Install testing dependencies
    test_deps = [
        ("pytest==7.4.3", "Testing framework"),
        ("pytest-asyncio==0.21.1", "Async testing"),
        ("httpx==0.25.2", "HTTP client for testing"),
    ]
    
    for dep, desc in test_deps:
        if not run_command(f"pip install {dep}", f"Installing {desc}"):
            print(f"⚠️  Warning: Failed to install {desc} (optional)")
    
    print("\n" + "="*50)
    print("🎉 Dependency Installation Complete!")
    print("="*50)
    
    print("\nNext steps:")
    print("1. Create .env file: cp env.example .env")
    print("2. Update .env with your database and email settings")
    print("3. Initialize database: python init_db.py")
    print("4. Start the server: python start.py")
    
    print("\nOptional dependencies (uncomment in requirements.txt if needed):")
    print("- redis==5.0.1 (for caching)")
    print("- celery==5.3.4 (for background tasks)")
    print("- stripe==7.8.0 (for payments)")

if __name__ == "__main__":
    main()
