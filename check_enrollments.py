#!/usr/bin/env python3
"""
Check enrollment records in the database
"""
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal
from sqlalchemy import text


def check_enrollments():
    """Check and display all enrollment records"""
    db = SessionLocal()
    
    try:
        print("📊 Checking Enrollment Records...\n")
        
        # Get all enrollments using raw SQL to avoid import issues
        result = db.execute(text("SELECT COUNT(*) FROM enrollments"))
        enrollment_count = result.scalar()
        
        if enrollment_count == 0:
            print("❌ No enrollment records found in the database.")
            print("✅ The enrollment forms are ready to receive data!")
            print("\n🔗 API Endpoint: /api/v1/enrollments/form")
            print("📱 Frontend forms are configured to submit to this endpoint.")
            return
        
        print(f"✅ Found {enrollment_count} enrollment record(s):\n")
        
        # Get detailed enrollment data
        enrollments_result = db.execute(text("""
            SELECT id, student_name, student_email, student_phone, student_city, 
                   course_title, course_price, status, enrolled_at, payment_method
            FROM enrollments 
            ORDER BY enrolled_at DESC
        """))
        
        enrollments = enrollments_result.fetchall()
        
        for i, enrollment in enumerate(enrollments, 1):
            print(f"📋 Enrollment #{i}:")
            print(f"   ID: {enrollment.id}")
            print(f"   Student: {enrollment.student_name}")
            print(f"   Email: {enrollment.student_email}")
            print(f"   Phone: {enrollment.student_phone}")
            print(f"   City: {enrollment.student_city}")
            print(f"   Course: {enrollment.course_title}")
            print(f"   Price: {enrollment.course_price}")
            print(f"   Status: {enrollment.status}")
            print(f"   Enrolled: {enrollment.enrolled_at}")
            print(f"   Payment Method: {enrollment.payment_method}")
            print("-" * 50)
        
        # Show total counts
        users_result = db.execute(text("SELECT COUNT(*) FROM users"))
        courses_result = db.execute(text("SELECT COUNT(*) FROM courses"))
        
        total_users = users_result.scalar()
        total_courses = courses_result.scalar()
        
        print(f"\n📈 Database Statistics:")
        print(f"   Total Users: {total_users}")
        print(f"   Total Courses: {total_courses}")
        print(f"   Total Enrollments: {enrollment_count}")
        
    except Exception as e:
        print(f"❌ Error checking enrollments: {e}")
        
    finally:
        db.close()


if __name__ == "__main__":
    check_enrollments()