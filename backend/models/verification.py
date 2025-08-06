import enum

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String, Text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

"""
Verification Model for EHB System
"""


class VerificationType(enum.Enum):
    """Verification types"""

    PSS = "pss"
    EMO = "emo"
    EDR = "edr"
    KYC = "kyc"
    EMAIL = "email"
    PHONE = "phone"
    DOCUMENT = "document"


class VerificationStatus(enum.Enum):
    """Verification status"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Verification(Base):
    """Verification model for EHB system"""

    __tablename__ = "verifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    verification_type = Column(Enum(VerificationType), nullable=False)
    status = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING)

    # Verification details
    document_type = Column(String(50), nullable=True)
    document_number = Column(String(100), nullable=True)
    document_url = Column(String(255), nullable=True)

    # Verification metadata
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    verified_at = Column(DateTime(timezone=True), nullable=True)
    verified_by = Column(String(100), nullable=True)

    # Verification notes
    notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    # Expiration
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_expired = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="verifications")

    def __repr__(self):
        return f"<Verification(id={self.id}, type='{self.verification_type.value}', status='{self.status.value}')>"
