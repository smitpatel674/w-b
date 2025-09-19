#!/usr/bin/env python3
"""
Add enrollment form fields to enrollments table
"""
from sqlalchemy import text
from app.database.database import engine


def add_enrollment_columns():
    """Add form data columns to enrollments table"""
    try:
        with engine.connect() as connection:
            # Add new columns to enrollments table
            columns_to_add = [
                ("student_name", "VARCHAR NOT NULL DEFAULT ''"),
                ("student_email", "VARCHAR NOT NULL DEFAULT ''"), 
                ("student_phone", "VARCHAR NOT NULL DEFAULT ''"),
                ("student_city", "VARCHAR NOT NULL DEFAULT ''"),
                ("course_title", "VARCHAR NOT NULL DEFAULT ''"),
                ("course_price", "VARCHAR NOT NULL DEFAULT ''")
            ]
            
            for column_name, column_type in columns_to_add:
                try:
                    # Check if column exists
                    result = connection.execute(text(f"""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'enrollments' AND column_name = '{column_name}'
                    """))
                    
                    if not result.fetchone():
                        # Add column
                        connection.execute(text(f"""
                            ALTER TABLE enrollments ADD COLUMN {column_name} {column_type}
                        """))
                        print(f"✅ Added column: {column_name}")
                    else:
                        print(f"✅ Column already exists: {column_name}")
                        
                except Exception as e:
                    print(f"⚠️  Warning adding {column_name}: {e}")
            
            connection.commit()
            print("\n🎉 Enrollment table updated successfully!")
            print("Now enrollment form data will be stored directly in the enrollments table.")
            
    except Exception as e:
        print(f"❌ Error updating enrollments table: {e}")
        raise


if __name__ == "__main__":
    add_enrollment_columns()