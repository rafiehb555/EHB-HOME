import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.sql import func

from .base import Base


class UserLevel(enum.Enum):
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))

    # EHB specific fields
    sql_level = Column(Enum(UserLevel), default=UserLevel.BASIC)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # Profile information
    avatar_url = Column(String(500))
    bio = Column(Text)
    company = Column(String(200))
    position = Column(String(100))

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Verification fields
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)
    kyc_verified = Column(Boolean, default=False)

    # Settings
    preferences = Column(Text)  # JSON string for user preferences
    notification_settings = Column(Text)  # JSON string for notification settings

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "sql_level": self.sql_level.value if self.sql_level else None,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "avatar_url": self.avatar_url,
            "company": self.company,
            "position": self.position,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "email_verified": self.email_verified,
            "phone_verified": self.phone_verified,
            "kyc_verified": self.kyc_verified,
        }
