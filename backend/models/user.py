"""
User Model for EHB System
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from .base import Base


class UserLevel(enum.Enum):
    """User SQL levels"""
    FREE = "free"
    BASIC = "basic"
    NORMAL = "normal"
    HIGH = "high"
    VIP = "vip"


class UserStatus(enum.Enum):
    """User status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class User(Base):
    """User model for EHB system"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)

    # User level and status
    sql_level = Column(Enum(UserLevel), default=UserLevel.FREE)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING)

    # Profile information
    avatar_url = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    address = Column(Text, nullable=True)
    country = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)

    # Verification flags
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)
    kyc_verified = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    wallets = relationship("Wallet", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    verifications = relationship("Verification", back_populates="user")
    franchises = relationship("Franchise", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', level='{self.sql_level.value}')>"
