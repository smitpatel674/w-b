#!/usr/bin/env python3
"""
Add city column to users table
"""
from sqlalchemy import text
from app.database.database import engine


def add_city_column():
    """Add city column to users table if it doesn't exist"""
    try:
        with engine.connect() as connection:
            # Check if city column exists
            result = connection.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'city'
            """))
            
            if not result.fetchone():
                # Add city column
                connection.execute(text("""
                    ALTER TABLE users ADD COLUMN city VARCHAR
                """))
                connection.commit()
                print("✅ City column added to users table")
            else:
                print("✅ City column already exists in users table")
                
    except Exception as e:
        print(f"❌ Error adding city column: {e}")


if __name__ == "__main__":
    add_city_column()