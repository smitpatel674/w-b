"""
Database migration script to create consultation_schedules table
Run this script to add the consultation scheduling functionality to your database
"""

import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection details
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:root@localhost:5432/wealth')

def create_consultation_table():
    """Create the consultation_schedules table"""
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS consultation_schedules (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        preferred_date VARCHAR(10) NOT NULL,
        preferred_time VARCHAR(5) NOT NULL,
        message TEXT,
        status VARCHAR(20) DEFAULT 'scheduled',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT TRUE
    );
    
    -- Create index for faster queries
    CREATE INDEX IF NOT EXISTS idx_consultation_schedules_date 
    ON consultation_schedules(preferred_date);
    
    CREATE INDEX IF NOT EXISTS idx_consultation_schedules_status 
    ON consultation_schedules(status);
    
    CREATE INDEX IF NOT EXISTS idx_consultation_schedules_email 
    ON consultation_schedules(email);
    """
    
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Execute the query
        cursor.execute(create_table_query)
        
        # Commit the changes
        conn.commit()
        
        print("✅ Successfully created consultation_schedules table")
        print("✅ Indexes created for optimal performance")
        
        # Close the connection
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creating consultation table: {e}")
        return False
    
    return True

def verify_table_creation():
    """Verify that the table was created successfully"""
    
    verify_query = """
    SELECT column_name, data_type, is_nullable 
    FROM information_schema.columns 
    WHERE table_name = 'consultation_schedules'
    ORDER BY ordinal_position;
    """
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute(verify_query)
        columns = cursor.fetchall()
        
        if columns:
            print("\n📋 Table structure:")
            print("Column Name".ljust(20) + "Data Type".ljust(20) + "Nullable")
            print("-" * 60)
            for column in columns:
                nullable = "YES" if column[2] == "YES" else "NO"
                print(f"{column[0].ljust(20)}{column[1].ljust(20)}{nullable}")
        else:
            print("❌ Table not found or no columns detected")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verifying table: {e}")

if __name__ == "__main__":
    print("🚀 Starting consultation table migration...")
    
    if create_consultation_table():
        verify_table_creation()
        print("\n✅ Migration completed successfully!")
        print("🎉 You can now use the consultation scheduling feature!")
    else:
        print("\n❌ Migration failed. Please check the errors above.")