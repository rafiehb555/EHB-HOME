#!/usr/bin/env python3
"""
Simple EHB Database Setup
Works with existing PostgreSQL instance
"""

import os
import sys
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.base import Base, engine, SessionLocal
from models.user import User
from models.service import Service, ServiceType, ServiceStatus
from models.transaction import Transaction
from models.wallet import Wallet
from models.franchise import Franchise
from models.verification import Verification


def test_postgresql_connection():
    """Test different PostgreSQL connection methods"""
    print("🔍 Testing PostgreSQL connections...")

    # Common connection configurations
    configs = [
        {"host": "localhost", "port": "5433", "database": "ehb_database", "user": "ehb_user", "password": "postgres"},
        {"host": "localhost", "port": "5433", "database": "postgres", "user": "ehb_user", "password": "postgres"},
        {"host": "localhost", "port": "5432", "database": "postgres", "user": "postgres", "password": ""},
        {"host": "localhost", "port": "5432", "database": "postgres", "user": "postgres", "password": "postgres"},
    ]

    for i, config in enumerate(configs, 1):
        try:
            print(f"  Testing config {i}: {config['user']}@{config['host']}:{config['port']}")
            conn = psycopg2.connect(**config)
            conn.close()
            print(f"✅ Success with config {i}!")
            return config
        except psycopg2.OperationalError as e:
            print(f"  ❌ Config {i} failed: {e}")
        except Exception as e:
            print(f"  ❌ Config {i} error: {e}")

    print("❌ No PostgreSQL connection method worked")
    return None


def create_database_schema():
    """Create database schema using SQLAlchemy"""
    print("🏗️ Creating database schema...")

    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating schema: {e}")
        return False


def insert_initial_data():
    """Insert initial data into the database"""
    print("📝 Inserting initial data...")

    try:
        db = SessionLocal()

        # Check if services already exist
        existing_services = db.query(Service).count()
        if existing_services > 0:
            print("✅ Initial data already exists!")
            db.close()
            return True

        # Insert default services
        services_data = [
            {
                "name": "Personal Security System",
                "service_type": ServiceType.PSS,
                "status": ServiceStatus.ACTIVE,
                "description": "Advanced personal security and verification system",
                "version": "1.0.0",
                "price_per_month": 29.99,
                "usage_limit": 1000,
                "endpoint_url": "http://pss:4001",
                "icon_url": "/static/icons/pss.png",
                "documentation_url": "https://docs.ehb.com/pss"
            },
            {
                "name": "Easy Management Office",
                "service_type": ServiceType.EMO,
                "status": ServiceStatus.ACTIVE,
                "description": "Comprehensive office management solution",
                "version": "1.0.0",
                "price_per_month": 49.99,
                "usage_limit": 2000,
                "endpoint_url": "http://emo:4003",
                "icon_url": "/static/icons/emo.png",
                "documentation_url": "https://docs.ehb.com/emo"
            },
            {
                "name": "Exam Decision Registration",
                "service_type": ServiceType.EDR,
                "status": ServiceStatus.ACTIVE,
                "description": "Educational examination and decision system",
                "version": "1.0.0",
                "price_per_month": 39.99,
                "usage_limit": 1500,
                "endpoint_url": "http://edr:4002",
                "icon_url": "/static/icons/edr.png",
                "documentation_url": "https://docs.ehb.com/edr"
            },
            {
                "name": "Job Profile System",
                "service_type": ServiceType.JPS,
                "status": ServiceStatus.ACTIVE,
                "description": "Professional job profile and career management",
                "version": "1.0.0",
                "price_per_month": 19.99,
                "usage_limit": 1000,
                "endpoint_url": "http://jps:4005",
                "icon_url": "/static/icons/jps.png",
                "documentation_url": "https://docs.ehb.com/jps"
            },
            {
                "name": "GoSellr E-commerce",
                "service_type": ServiceType.GOSELLR,
                "status": ServiceStatus.ACTIVE,
                "description": "Complete e-commerce platform for businesses",
                "version": "1.0.0",
                "price_per_month": 79.99,
                "usage_limit": 5000,
                "endpoint_url": "http://gosellr:4004",
                "icon_url": "/static/icons/gosellr.png",
                "documentation_url": "https://docs.ehb.com/gosellr"
            }
        ]

        for service_data in services_data:
            service = Service(**service_data)
            db.add(service)

        db.commit()
        print("✅ Initial services inserted successfully!")
        db.close()
        return True

    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return False


def test_database_connection():
    """Test the database connection"""
    print("🧪 Testing database connection...")

    try:
        with SessionLocal() as session:
            # Test basic connection
            result = session.execute(text("SELECT 1"))
            print("✅ Database connection test successful!")

            # Test service count
            service_count = session.query(Service).count()
            print(f"✅ Found {service_count} services in database")

            # Test database name
            result = session.execute(text("SELECT current_database()"))
            db_name = result.fetchone()[0]
            print(f"✅ Connected to database: {db_name}")

        return True

    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Simple EHB Database Setup")
    print("=" * 50)

    # Step 1: Test PostgreSQL connection
    config = test_postgresql_connection()
    if not config:
        print("❌ Cannot proceed without PostgreSQL connection")
        print("\n💡 Try one of these solutions:")
        print("1. Install PostgreSQL locally")
        print("2. Use Docker: docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:15")
        print("3. Check if PostgreSQL is running on a different port")
        return False

    # Step 2: Create schema
    if not create_database_schema():
        print("❌ Failed to create schema")
        return False

    # Step 3: Insert initial data
    if not insert_initial_data():
        print("❌ Failed to insert initial data")
        return False

    # Step 4: Test connection
    if not test_database_connection():
        print("❌ Database test failed")
        return False

    print("\n🎉 Database setup completed successfully!")
    print("=" * 50)
    print("📊 Database: Connected to existing PostgreSQL")
    print("🔗 Connection: Working with SQLAlchemy")
    print("📝 Services: 5 default services inserted")
    print("=" * 50)

    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ EHB database is ready for development!")
    else:
        print("\n❌ Database setup failed!")
        sys.exit(1)
