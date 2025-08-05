#!/usr/bin/env python3
"""
EHB Database Setup Script
Initializes the database with tables and default data
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from models.database.connection import create_tables, init_db, engine
from sqlalchemy import text

def test_database_connection():
    """Test if we can connect to the database"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def setup_database():
    """Setup the complete database"""
    print("🔧 Setting up EHB Database...")

    # Test connection first
    if not test_database_connection():
        print("❌ Cannot proceed without database connection")
        return False

    try:
        # Create tables
        print("📋 Creating database tables...")
        create_tables()
        print("✅ Tables created successfully!")

        # Initialize with default data
        print("📊 Initializing with default data...")
        init_db()
        print("✅ Default data initialized!")

        print("🎉 Database setup completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Error during database setup: {e}")
        return False

def main():
    """Main function"""
    print("🚀 EHB Database Setup")
    print("=" * 50)

    success = setup_database()

    if success:
        print("\n✅ Database is ready!")
        print("📊 You can now:")
        print("   - Start the backend server")
        print("   - Access the admin panel")
        print("   - Use the API endpoints")
    else:
        print("\n❌ Database setup failed!")
        print("🔧 Please check:")
        print("   - PostgreSQL is running")
        print("   - Database credentials are correct")
        print("   - Docker container is active")

if __name__ == "__main__":
    main()
