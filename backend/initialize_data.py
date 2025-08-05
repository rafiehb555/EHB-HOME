#!/usr/bin/env python3
"""
Initialize Default Data Script
Creates admin user and default services
"""

import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session
from utils.database.connection import SessionLocal, engine
from models.database.user import User, UserLevel
from models.database.service import Service, ServiceType, ServiceStatus
from models.database.transaction import Transaction, TransactionType, TransactionStatus
from models.database.transaction import Wallet
from services.auth.jwt import get_password_hash


def create_admin_user():
    """Create default admin user"""
    try:
        db = SessionLocal()

        # Check if admin user already exists
        admin = db.query(User).filter(User.email == "admin@ehb.com").first()
        if admin:
            print("✅ Admin user already exists")
            return admin

        # Create admin user
        admin_password = "admin123"  # Change this in production
        hashed_password = get_password_hash(admin_password)

        admin_user = User(
            email="admin@ehb.com",
            username="admin",
            password_hash=hashed_password,
            first_name="EHB",
            last_name="Administrator",
            sql_level=UserLevel.ADMIN,
            is_admin=True,
            is_verified=True,
            is_active=True,
            email_verified=True
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"✅ Admin user created: {admin_user.email}")
        return admin_user

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return None
    finally:
        db.close()


def create_default_services():
    """Create default EHB services"""
    try:
        db = SessionLocal()

        # Check if services already exist
        existing_services = db.query(Service).count()
        if existing_services > 0:
            print(f"✅ {existing_services} services already exist")
            return

        # Default services configuration
        default_services = [
            {
                "name": "Personal Security System (PSS)",
                "type": ServiceType.PSS,
                "port": 4001,
                "description": "Advanced personal security and verification system",
                "version": "1.0.0"
            },
            {
                "name": "Easy Management Office (EMO)",
                "type": ServiceType.EMO,
                "port": 4003,
                "description": "Comprehensive office management solution",
                "version": "1.0.0"
            },
            {
                "name": "Exam Decision Registration (EDR)",
                "type": ServiceType.EDR,
                "port": 4002,
                "description": "Educational examination and decision system",
                "version": "1.0.0"
            },
            {
                "name": "Job Profile System (JPS)",
                "type": ServiceType.JPS,
                "port": 4005,
                "description": "Professional job profile and career management",
                "version": "1.0.0"
            },
            {
                "name": "GoSellr E-commerce",
                "type": ServiceType.GOSELLR,
                "port": 4004,
                "description": "Complete e-commerce platform for businesses",
                "version": "1.0.0"
            },
            {
                "name": "EHB Wallet",
                "type": ServiceType.WALLET,
                "port": 5001,
                "description": "Multi-chain cryptocurrency wallet",
                "version": "1.0.0"
            },
            {
                "name": "AI Agent",
                "type": ServiceType.AI_AGENT,
                "port": 4007,
                "description": "Intelligent AI agent services",
                "version": "1.0.0"
            },
            {
                "name": "AI Robot",
                "type": ServiceType.AI_ROBOT,
                "port": 4008,
                "description": "Advanced AI robot automation",
                "version": "1.0.0"
            }
        ]

        created_services = []
        for service_data in default_services:
            service = Service(
                name=service_data["name"],
                type=service_data["type"],
                status=ServiceStatus.ACTIVE,
                port=service_data["port"],
                host="localhost",
                description=service_data["description"],
                version=service_data["version"],
                is_healthy=True
            )
            db.add(service)
            created_services.append(service)

        db.commit()

        for service in created_services:
            print(f"✅ Service created: {service.name} (Port: {service.port})")

        print(f"✅ Created {len(created_services)} default services")

    except Exception as e:
        print(f"❌ Error creating services: {e}")
        db.rollback()
    finally:
        db.close()


def create_admin_wallet():
    """Create wallet for admin user"""
    try:
        db = SessionLocal()

        # Get admin user
        admin = db.query(User).filter(User.email == "admin@ehb.com").first()
        if not admin:
            print("❌ Admin user not found")
            return

        # Check if admin wallet already exists
        existing_wallet = db.query(Wallet).filter(Wallet.user_id == admin.id).first()
        if existing_wallet:
            print("✅ Admin wallet already exists")
            return

        # Create admin wallet
        admin_wallet = Wallet(
            user_id=admin.id,
            balance=1000.00,  # Initial balance
            currency="USD",
            is_active=True
        )

        db.add(admin_wallet)
        db.commit()

        print(f"✅ Admin wallet created with balance: ${admin_wallet.balance}")

    except Exception as e:
        print(f"❌ Error creating admin wallet: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Main initialization function"""
    print("=" * 60)
    print("🚀 EHB System Data Initialization")
    print("=" * 60)
    print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        # Test database connection
        print("🔍 Testing database connection...")
        from utils.database.connection import test_connection
        if not test_connection():
            print("❌ Database connection failed")
            return False
        print("✅ Database connection successful")

        # Create admin user
        print("\n👤 Creating admin user...")
        admin = create_admin_user()
        if not admin:
            return False

        # Create default services
        print("\n🔧 Creating default services...")
        create_default_services()

        # Create admin wallet
        print("\n💰 Creating admin wallet...")
        create_admin_wallet()

        print("\n" + "=" * 60)
        print("🎉 Data Initialization Complete!")
        print("=" * 60)
        print("📋 Summary:")
        print("✅ Admin user: admin@ehb.com")
        print("✅ Default services: 8 services created")
        print("✅ Admin wallet: $1000.00 initial balance")
        print("\n🔑 Login Credentials:")
        print("   Email: admin@ehb.com")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n⚠️  Remember to change the admin password in production!")

        return True

    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
