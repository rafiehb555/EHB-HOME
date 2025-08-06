import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from models.base import Base, engine, SessionLocal
from models.user import User
from models.service import Service, ServiceType, ServiceStatus
from models.transaction import Transaction
from models.wallet import Wallet
from models.franchise import Franchise
from models.verification import Verification


"""
Database Setup Script for EHB System
"""

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

load_dotenv()


def create_database():
    """Create all database tables"""
    print("🗄️  Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    return True


def insert_initial_data():
    """Insert initial data into the database"""
    print("📝 Inserting initial data...")

    db = SessionLocal()
    try:
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
                "documentation_url": "https://docs.ehb.com/pss",
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
                "documentation_url": "https://docs.ehb.com/emo",
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
                "documentation_url": "https://docs.ehb.com/edr",
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
                "documentation_url": "https://docs.ehb.com/jps",
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
                "documentation_url": "https://docs.ehb.com/gosellr",
            },
            {
                "name": "EHB Wallet",
                "service_type": ServiceType.WALLET,
                "status": ServiceStatus.ACTIVE,
                "description": "Multi-chain cryptocurrency wallet",
                "version": "1.0.0",
                "price_per_month": 0.00,
                "usage_limit": 10000,
                "endpoint_url": "http://wallet:5001",
                "icon_url": "/static/icons/wallet.png",
                "documentation_url": "https://docs.ehb.com/wallet",
            },
            {
                "name": "Franchise Management",
                "service_type": ServiceType.FRANCHISE,
                "status": ServiceStatus.ACTIVE,
                "description": "Franchise application and management system",
                "version": "1.0.0",
                "price_per_month": 99.99,
                "usage_limit": 500,
                "endpoint_url": "http://franchise:4006",
                "icon_url": "/static/icons/franchise.png",
                "documentation_url": "https://docs.ehb.com/franchise",
            },
            {
                "name": "AI Marketplace",
                "service_type": ServiceType.AI_MARKETPLACE,
                "status": ServiceStatus.ACTIVE,
                "description": "AI services marketplace",
                "version": "1.0.0",
                "price_per_month": 59.99,
                "usage_limit": 3000,
                "endpoint_url": "http://ai-marketplace:4007",
                "icon_url": "/static/icons/ai-marketplace.png",
                "documentation_url": "https://docs.ehb.com/ai-marketplace",
            },
            {
                "name": "AI Agent",
                "service_type": ServiceType.AI_AGENT,
                "status": ServiceStatus.ACTIVE,
                "description": "Intelligent AI agent services",
                "version": "1.0.0",
                "price_per_month": 39.99,
                "usage_limit": 2000,
                "endpoint_url": "http://ai-agent:4008",
                "icon_url": "/static/icons/ai-agent.png",
                "documentation_url": "https://docs.ehb.com/ai-agent",
            },
            {
                "name": "AI Robot",
                "service_type": ServiceType.AI_ROBOT,
                "status": ServiceStatus.ACTIVE,
                "description": "Advanced AI robot automation",
                "version": "1.0.0",
                "price_per_month": 89.99,
                "usage_limit": 1000,
                "endpoint_url": "http://ai-robot:4009",
                "icon_url": "/static/icons/ai-robot.png",
                "documentation_url": "https://docs.ehb.com/ai-robot",
            },
        ]

        for service_data in services_data:
            # Check if service already exists
            existing_service = (
                db.query(Service)
                .filter(Service.service_type == service_data["service_type"])
                .first()
            )

            if not existing_service:
                service = Service(**service_data)
                db.add(service)
                print(f"✅ Added service: {service_data['name']}")

        db.commit()
        print("✅ Initial data inserted successfully")

    except Exception as e:
        print(f"❌ Error inserting initial data: {e}")
        db.rollback()
        return False
    finally:
        db.close()

    return True


def create_database_views():
    """Create database views for statistics"""
    print("📊 Creating database views...")

    try:
        with engine.connect() as conn:
            # User statistics view
            conn.execute(
                text(
                    """
                CREATE OR REPLACE VIEW user_statistics AS
                SELECT
                    COUNT(*) as total_users,
                    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_users,
                    COUNT(CASE WHEN email_verified = true THEN 1 END) as verified_users,
                    COUNT(CASE WHEN sql_level = 'vip' THEN 1 END) as vip_users,
                    COUNT(CASE WHEN created_at >= CURRENT_DATE - INTERVAL '30 days' THEN 1 END) as new_users_30_days
                FROM users
            """
                )
            )

            # Transaction statistics view
            conn.execute(
                text(
                    """
                CREATE OR REPLACE VIEW transaction_statistics AS
                SELECT
                    COUNT(*) as total_transactions,
                    COALESCE(SUM(amount), 0) as total_volume,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_transactions,
                    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_transactions,
                    COALESCE(AVG(amount), 0) as average_transaction_amount
                FROM transactions
            """
                )
            )

            conn.commit()
            print("✅ Database views created successfully")

    except Exception as e:
        print(f"❌ Error creating views: {e}")
        return False

    return True


def main():
    """Main setup function"""
    print("🚀 Starting EHB Database Setup...")

    # Create tables
    if not create_database():
        print("❌ Failed to create database tables")
        return

    # Insert initial data
    if not insert_initial_data():
        print("❌ Failed to insert initial data")
        return

    # Create views
    if not create_database_views():
        print("❌ Failed to create database views")
        return

    print("🎉 EHB Database setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run 'alembic revision --autogenerate -m \"Initial migration\"'")
    print("2. Run 'alembic upgrade head' to apply migrations")
    print("3. Start your application with 'python -m uvicorn app.main:app --reload'")


if __name__ == "__main__":
    main()
