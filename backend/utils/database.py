"""
Database utilities for EHB system
"""

from sqlalchemy.orm import Session
from typing import Generator
from models.base import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_connection() -> bool:
    """Check if database connection is working"""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def get_database_stats(db: Session) -> dict:
    """Get database statistics"""
    try:
        # Get table counts
        user_count = db.execute("SELECT COUNT(*) FROM users").scalar()
        service_count = db.execute("SELECT COUNT(*) FROM services").scalar()
        transaction_count = db.execute("SELECT COUNT(*) FROM transactions").scalar()
        wallet_count = db.execute("SELECT COUNT(*) FROM wallets").scalar()
        franchise_count = db.execute("SELECT COUNT(*) FROM franchises").scalar()
        verification_count = db.execute("SELECT COUNT(*) FROM verifications").scalar()

        return {
            "users": user_count or 0,
            "services": service_count or 0,
            "transactions": transaction_count or 0,
            "wallets": wallet_count or 0,
            "franchises": franchise_count or 0,
            "verifications": verification_count or 0
        }
    except Exception as e:
        print(f"❌ Error getting database stats: {e}")
        return {
            "users": 0,
            "services": 0,
            "transactions": 0,
            "wallets": 0,
            "franchises": 0,
            "verifications": 0
        }
