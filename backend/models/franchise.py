from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    Enum,
    Float,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from .base import Base


"""
Franchise Model for EHB System
"""


class FranchiseStatus(enum.Enum):
    """Franchise status"""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CLOSED = "closed"


class FranchiseType(enum.Enum):
    """Franchise types"""

    RETAIL = "retail"
    SERVICE = "service"
    FOOD = "food"
    TECHNOLOGY = "technology"
    EDUCATION = "education"
    HEALTHCARE = "healthcare"


class Franchise(Base):
    """Franchise model for EHB system"""

    __tablename__ = "franchises"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    franchise_type = Column(Enum(FranchiseType), nullable=False)
    status = Column(Enum(FranchiseStatus), default=FranchiseStatus.PENDING)

    # Basic information
    business_name = Column(String(100), nullable=False)
    business_description = Column(Text, nullable=True)
    industry = Column(String(50), nullable=True)

    # Location
    address = Column(Text, nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    postal_code = Column(String(20), nullable=True)

    # Contact information
    contact_person = Column(String(100), nullable=False)
    contact_email = Column(String(100), nullable=False)
    contact_phone = Column(String(20), nullable=False)

    # Financial information
    investment_amount = Column(Float, nullable=True)
    expected_revenue = Column(Float, nullable=True)
    franchise_fee = Column(Float, nullable=True)

    # Documents
    business_plan_url = Column(String(255), nullable=True)
    financial_statement_url = Column(String(255), nullable=True)
    legal_documents_url = Column(String(255), nullable=True)

    # Review information
    review_notes = Column(Text, nullable=True)
    reviewed_by = Column(String(100), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="franchises")

    def __repr__(self):
        return f"<Franchise(id={self.id}, business_name='{self.business_name}', status='{self.status.value}')>"
