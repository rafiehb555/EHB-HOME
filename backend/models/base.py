import os

from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
Database Configuration for EHB System
"""

load_dotenv()

# Database URL - using Docker PostgreSQL container
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://ehb_user:postgres@localhost:5433/ehb_database"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Create metadata for Alembic
db_metadata = MetaData()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Drop all database tables"""
    Base.metadata.drop_all(bind=engine)
