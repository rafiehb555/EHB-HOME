import os
import sys

from sqlalchemy.orm import Session

from backend.models.database.service import Service, ServiceLog
from backend.models.database.transaction import Transaction, Wallet
from backend.models.database.user import User
from backend.utils.database.connection import (SessionLocal, create_tables,
                                               test_connection)

#!/usr/bin/env python3
"""
Database Connection Test Script
Tests the PostgreSQL database connection and creates tables
"""

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("🔍 Testing Database Connection...")

    # Test connection
    if test_connection():
        print("✅ Database connection successful!")

        # Create tables
        print("📋 Creating database tables...")
        try:
            create_tables()
            print("✅ Database tables created successfully!")

            # Test data insertion
            print("📊 Testing data insertion...")
            db = SessionLocal()

            # Create test service
            test_service = Service(
                name="Test Service",
                service_type="pss",
                port=4001,
                status="active",
                description="Test service for database connection"
            )

            db.add(test_service)
            db.commit()
            db.refresh(test_service)

            print(f"✅ Test service created with ID: {test_service.id}")

            # Clean up
            db.delete(test_service)
            db.commit()
            db.close()

            print("✅ Database test completed successfully!")
            return True

        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
    else:
        print("❌ Database connection failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
