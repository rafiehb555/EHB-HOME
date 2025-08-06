import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .service import Service, ServiceStatus, ServiceType, UserService
from .transaction import Transaction, Wallet
from .user import User, UserLevel

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ehb_user:ehb_password@localhost:5432/ehb_database"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False  # Set to True for SQL query logging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables"""
    # Import all models to register them with Base
    # Create all tables
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all database tables"""
    Base.metadata.drop_all(bind=engine)





def init_db():
    """Initialize database with default data"""
    db = SessionLocal()
    try:
        # Import models
        # Check if tables are empty
        user_count = db.query(User).count()
        service_count = db.query(Service).count()

        if user_count == 0 and service_count == 0:
            # Create default services
            default_services = [
                {
                    "name": "PSS - KYC Verification",
                    "type": ServiceType.PSS,
                    "status": ServiceStatus.ACTIVE,
                    "port": 4001,
                    "host": "localhost",
                    "endpoint": "/api/v1/pss",
                    "description": "Personal Security Service for KYC verification",
                    "version": "1.0.0"
                },
                {
                    "name": "EMO - Business Verification",
                    "type": ServiceType.EMO,
                    "status": ServiceStatus.ACTIVE,
                    "port": 4003,
                    "host": "localhost",
                    "endpoint": "/api/v1/emo",
                    "description": "Enterprise Management Office for business verification",
                    "version": "1.0.0"
                },
                {
                    "name": "EDR - Skill Testing",
                    "type": ServiceType.EDR,
                    "status": ServiceStatus.ACTIVE,
                    "port": 4002,
                    "host": "localhost",
                    "endpoint": "/api/v1/edr",
                    "description": "Expert Development and Research for skill testing",
                    "version": "1.0.0"
                },
                {
                    "name": "JPS - Job Profile",
                    "type": ServiceType.JPS,
                    "status": ServiceStatus.ACTIVE,
                    "port": 4005,
                    "host": "localhost",
                    "endpoint": "/api/v1/jps",
                    "description": "Job Profile Service for career management",
                    "version": "1.0.0"
                },
                {
                    "name": "GoSellr - E-commerce",
                    "type": ServiceType.GOSELLR,
                    "status": ServiceStatus.ACTIVE,
                    "port": 4004,
                    "host": "localhost",
                    "endpoint": "/api/v1/gosellr",
                    "description": "E-commerce marketplace platform",
                    "version": "1.0.0"
                },
                {
                    "name": "Wallet - Payments",
                    "type": ServiceType.WALLET,
                    "status": ServiceStatus.ACTIVE,
                    "port": 5001,
                    "host": "localhost",
                    "endpoint": "/api/v1/wallet",
                    "description": "Digital wallet for payments and transactions",
                    "version": "1.0.0"
                },
                {
                    "name": "AI Agent",
                    "type": ServiceType.AI_AGENT,
                    "status": ServiceStatus.ACTIVE,
                    "port": 4007,
                    "host": "localhost",
                    "endpoint": "/api/v1/ai-agent",
                    "description": "AI-powered virtual assistant",
                    "version": "1.0.0"
                },
                {
                    "name": "AI Robot",
                    "type": ServiceType.AI_ROBOT,
                    "status": ServiceStatus.ACTIVE,
                    "port": 4008,
                    "host": "localhost",
                    "endpoint": "/api/v1/ai-robot",
                    "description": "Automated AI workflow system",
                    "version": "1.0.0"
                }
            ]

            for service_data in default_services:
                service = Service(**service_data)
                db.add(service)

            # Create admin user
            admin_user = User(
                email="admin@ehb.com",
                username="admin",
                password_hash="admin_hash",  # Will be hashed properly in auth system
                first_name="Admin",
                last_name="User",
                sql_level=UserLevel.ADMIN,
                is_verified=True,
                is_active=True,
                is_admin=True,
                email_verified=True,
                phone_verified=True,
                kyc_verified=True
            )
            db.add(admin_user)

            db.commit()
            print("✅ Database initialized with default data")
        else:
            print("ℹ️ Database already contains data, skipping initialization")

    except Exception as e:
        db.rollback()
        print(f"❌ Error initializing database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🔧 Setting up database...")
    create_tables()
    init_db()
    print("✅ Database setup complete!")
