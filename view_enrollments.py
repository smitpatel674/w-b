#!/usr/bin/env python3
"""
View enrollment data from database
"""
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.enrollment import Enrollment
from app.models.user import User
from app.models.course import Course


def view_enrollments():
    """Display all enrollment data"""
    db = SessionLocal()
    
    try:
        enrollments = db.query(Enrollment).all()
        
        if not enrollments:
            print("📝 No enrollments found in database yet.")
            print("\n💡 To test:")
            print("1. Go to http://localhost:5174")
            print("2. Click 'Enroll Now' on any course")
            print("3. Fill the form and submit")
            print("4. Run this script again to see the data")
            return
        
        print("📊 ENROLLMENT DATA:")
        print("=" * 80)
        
        for i, enrollment in enumerate(enrollments, 1):
            print(f"\n📋 Enrollment #{i}")
            print(f"   ID: {enrollment.id}")
            print(f"   👤 Student Name: {enrollment.student_name}")
            print(f"   📧 Email: {enrollment.student_email}")
            print(f"   📱 Phone: {enrollment.student_phone}")
            print(f"   🏙️  City: {enrollment.student_city}")
            print(f"   📚 Course: {enrollment.course_title}")
            print(f"   💰 Price: {enrollment.course_price}")
            print(f"   📅 Enrolled: {enrollment.enrolled_at}")
            print(f"   📊 Status: {enrollment.status}")
            print("-" * 50)
            
        print(f"\n✅ Total enrollments: {len(enrollments)}")
        
    except Exception as e:
        print(f"❌ Error viewing enrollments: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    view_enrollments()