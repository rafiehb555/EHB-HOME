#!/usr/bin/env python3
"""
EHB Database Setup Script
Works with existing PostgreSQL instance
"""

import os
import sys
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import time

# Add the parent directory to the path so we can import our models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.base import Base, engine, SessionLocal
from models import *  # Import all models
from database.setup import main as setup_database


def check_postgresql_connection():
    """Check if PostgreSQL is accessible"""
    print("🔍 Checking PostgreSQL connection...")

    try:
        # Try to connect to PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="postgres",
            password="postgres"
        )
        conn.close()
        print("✅ PostgreSQL connection successful!")
        return True
    except psycopg2.OperationalError as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def create_ehb_database():
    """Create EHB database and user"""
    print("🗄️ Creating EHB database...")

    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="postgres",
            password="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'ehb_database'")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE ehb_database")
            print("✅ Database 'ehb_database' created!")
        else:
            print("✅ Database 'ehb_database' already exists!")

        # Create user if it doesn't exist
        cursor.execute("SELECT 1 FROM pg_user WHERE usename = 'ehb_user'")
        if not cursor.fetchone():
            cursor.execute("CREATE USER ehb_user WITH PASSWORD 'ehb_password'")
            print("✅ User 'ehb_user' created!")
        else:
            print("✅ User 'ehb_user' already exists!")

        # Grant privileges
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE ehb_database TO ehb_user")
        print("✅ Privileges granted!")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False


def setup_database_schema():
    """Set up database schema and initial data"""
    print("🏗️ Setting up database schema...")

    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created!")

        # Run the setup script
        setup_database()
        print("✅ Initial data inserted!")

        return True

    except Exception as e:
        print(f"❌ Error setting up schema: {e}")
        return False


def run_migrations():
    """Run Alembic migrations"""
    print("🔄 Running database migrations...")

    try:
        # Initialize Alembic if not already done
        if not os.path.exists("alembic/versions"):
            os.system("alembic init alembic")

        # Create initial migration
        os.system("alembic revision --autogenerate -m 'Initial migration'")

        # Run migrations
        os.system("alembic upgrade head")
        print("✅ Migrations completed!")

        return True

    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False


def test_database_connection():
    """Test the database connection with our models"""
    print("🧪 Testing database connection...")

    try:
        # Test connection
        with SessionLocal() as session:
            result = session.execute(text("SELECT 1"))
            print("✅ Database connection test successful!")

            # Test a simple query
            result = session.execute(text("SELECT current_database()"))
            db_name = result.fetchone()[0]
            print(f"✅ Connected to database: {db_name}")

        return True

    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 EHB Database Setup")
    print("=" * 50)

    # Step 1: Check PostgreSQL connection
    if not check_postgresql_connection():
        print("❌ Cannot proceed without PostgreSQL connection")
        return False

    # Step 2: Create database and user
    if not create_ehb_database():
        print("❌ Failed to create database")
        return False

    # Step 3: Set up schema
    if not setup_database_schema():
        print("❌ Failed to set up schema")
        return False

    # Step 4: Run migrations
    if not run_migrations():
        print("❌ Failed to run migrations")
        return False

    # Step 5: Test connection
    if not test_database_connection():
        print("❌ Database test failed")
        return False

    print("\n🎉 Database setup completed successfully!")
    print("=" * 50)
    print("📊 Database: ehb_database")
    print("👤 User: ehb_user")
    print("🔗 Connection: postgresql://ehb_user:ehb_password@localhost:5432/ehb_database")
    print("=" * 50)

    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ EHB database is ready for development!")
    else:
        print("\n❌ Database setup failed!")
        sys.exit(1)
