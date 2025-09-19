#!/usr/bin/env python3
"""
Direct SQL query to view enrollment data
"""
from sqlalchemy import text
from app.database.database import engine


def query_enrollment_data():
    """Query enrollment data directly using SQL"""
    try:
        with engine.connect() as connection:
            # Check if enrollment table has the new columns
            result = connection.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'enrollments' 
                ORDER BY ordinal_position
            """))
            
            columns = [row[0] for row in result.fetchall()]
            print("📋 Enrollment table columns:")
            for col in columns:
                print(f"   - {col}")
            
            # Query enrollment data
            result = connection.execute(text("""
                SELECT 
                    id,
                    student_name,
                    student_email, 
                    student_phone,
                    student_city,
                    course_title,
                    course_price,
                    enrolled_at,
                    status
                FROM enrollments 
                ORDER BY enrolled_at DESC
            """))
            
            enrollments = result.fetchall()
            
            if not enrollments:
                print("\n📝 No enrollments found.")
                print("\n💡 Test the enrollment form:")
                print("1. Go to: http://localhost:5174")
                print("2. Click 'Enroll Now' on any course")
                print("3. Fill: Name, City, Phone, Email")
                print("4. Submit the form")
                print("5. Check here for the data!")
            else:
                print(f"\n📊 Found {len(enrollments)} enrollments:")
                print("=" * 80)
                
                for enrollment in enrollments:
                    print(f"\n📋 Enrollment ID: {enrollment[0]}")
                    print(f"   👤 Name: {enrollment[1] or 'Not stored'}")
                    print(f"   📧 Email: {enrollment[2] or 'Not stored'}")
                    print(f"   📱 Phone: {enrollment[3] or 'Not stored'}")
                    print(f"   🏙️  City: {enrollment[4] or 'Not stored'}")
                    print(f"   📚 Course: {enrollment[5] or 'Not stored'}")
                    print(f"   💰 Price: {enrollment[6] or 'Not stored'}")
                    print(f"   📅 Date: {enrollment[7]}")
                    print(f"   📊 Status: {enrollment[8]}")
                    print("-" * 50)
                    
    except Exception as e:
        print(f"❌ Error querying database: {e}")


if __name__ == "__main__":
    query_enrollment_data()