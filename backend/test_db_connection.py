#!/usr/bin/env python3
"""
Test Database Connection
"""

import psycopg2
import os

# Set the database URL environment variable
os.environ['DATABASE_URL'] = 'postgresql://ehb_user:postgres@localhost:5433/ehb_database'

def test_connection():
    """Test direct PostgreSQL connection"""
    print("🔍 Testing PostgreSQL connection...")

    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5433",
            database="ehb_database",
            user="ehb_user",
            password="postgres"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL connection successful!")
        print(f"📊 Version: {version[0]}")

        cursor.execute("SELECT current_database();")
        db_name = cursor.fetchone()
        print(f"📊 Database: {db_name[0]}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def test_sqlalchemy():
    """Test SQLAlchemy connection"""
    print("\n🔍 Testing SQLAlchemy connection...")

    try:
        from sqlalchemy import create_engine, text

        # Create engine with the correct URL
        engine = create_engine(
            "postgresql://ehb_user:postgres@localhost:5433/ehb_database",
            echo=False
        )

        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ SQLAlchemy connection successful!")

            result = conn.execute(text("SELECT current_database()"))
            db_name = result.fetchone()[0]
            print(f"📊 Connected to: {db_name}")

        return True

    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        return False


def main():
    """Main test function"""
    print("🚀 Database Connection Test")
    print("=" * 50)

    # Test 1: Direct PostgreSQL connection
    if not test_connection():
        print("❌ Direct PostgreSQL connection failed")
        return False

    # Test 2: SQLAlchemy connection
    if not test_sqlalchemy():
        print("❌ SQLAlchemy connection failed")
        return False

    print("\n🎉 All database connection tests passed!")
    print("=" * 50)
    print("📊 Database: ehb_database")
    print("👤 User: ehb_user")
    print("🔗 Connection: postgresql://ehb_user:postgres@localhost:5433/ehb_database")
    print("=" * 50)

    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Database connection is working!")
    else:
        print("\n❌ Database connection test failed!")
