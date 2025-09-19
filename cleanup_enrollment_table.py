"""
Script to remove unnecessary columns from the enrollments table
"""
import os
import sys
from sqlalchemy import text

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal, engine


def cleanup_enrollment_table():
    """Remove unnecessary columns from enrollments table"""
    
    session = SessionLocal()
    try:
        print("Starting cleanup of enrollments table...")
        
        # List of columns to remove (unnecessary for trading institute)
        columns_to_remove = [
            'completed_at',          # Can be derived from status
            'progress_percentage',   # Not needed for simple enrollment
            'certificate_issued',    # Certificates handled separately
            'certificate_url',       # Certificates handled separately
            'stripe_payment_intent_id'  # Too specific to Stripe
        ]
        
        # Check current table structure
        print("\nChecking current table structure...")
        result = session.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'enrollments' 
            ORDER BY ordinal_position;
        """))
        
        current_columns = result.fetchall()
        print("Current columns:")
        for col in current_columns:
            print(f"  - {col.column_name} ({col.data_type}, nullable: {col.is_nullable})")
        
        # Remove unnecessary columns
        print(f"\nRemoving {len(columns_to_remove)} unnecessary columns...")
        
        for column in columns_to_remove:
            try:
                # Check if column exists before trying to drop it
                check_result = session.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'enrollments' 
                    AND column_name = '{column}';
                """))
                
                if check_result.fetchone():
                    print(f"  Dropping column: {column}")
                    session.execute(text(f"ALTER TABLE enrollments DROP COLUMN IF EXISTS {column};"))
                else:
                    print(f"  Column {column} doesn't exist, skipping...")
                    
            except Exception as e:
                print(f"  Error dropping {column}: {e}")
                continue
        
        # Commit all changes
        session.commit()
        print("\nSuccessfully removed unnecessary columns!")
        
        # Show final table structure
        print("\nFinal table structure:")
        result = session.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'enrollments' 
            ORDER BY ordinal_position;
        """))
        
        final_columns = result.fetchall()
        for col in final_columns:
            print(f"  - {col.column_name} ({col.data_type}, nullable: {col.is_nullable})")
        
        # Show sample data with clean structure
        print("\nSample enrollment data (clean structure):")
        result = session.execute(text("""
            SELECT id, student_name, student_email, student_phone, student_city, 
                   course_title, course_price, status, enrolled_at, payment_amount, payment_method
            FROM enrollments 
            ORDER BY enrolled_at DESC 
            LIMIT 5;
        """))
        
        enrollments = result.fetchall()
        if enrollments:
            print("Recent enrollments:")
            for enrollment in enrollments:
                print(f"  ID: {enrollment.id}")
                print(f"    Student: {enrollment.student_name} ({enrollment.student_email})")
                print(f"    Phone: {enrollment.student_phone}, City: {enrollment.student_city}")
                print(f"    Course: {enrollment.course_title} - {enrollment.course_price}")
                print(f"    Status: {enrollment.status}, Enrolled: {enrollment.enrolled_at}")
                print(f"    Payment: {enrollment.payment_amount} via {enrollment.payment_method}")
                print("    " + "-" * 50)
        else:
            print("  No enrollment data found.")
            
    except Exception as e:
        print(f"Error during cleanup: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    print("Enrollment Table Cleanup Script")
    print("=" * 40)
    cleanup_enrollment_table()