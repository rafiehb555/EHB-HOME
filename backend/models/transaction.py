"""
Transaction Model for EHB System
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from .base import Base


class TransactionType(enum.Enum):
    """Transaction types"""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PAYMENT = "payment"
    REFUND = "refund"
    FEE = "fee"
    REWARD = "reward"


class TransactionStatus(enum.Enum):
    """Transaction status"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Transaction(Base):
    """Transaction model for EHB system"""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_hash = Column(String(255), unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Transaction details
    transaction_type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")

    # Blockchain details
    blockchain_network = Column(String(50), nullable=True)
    from_address = Column(String(255), nullable=True)
    to_address = Column(String(255), nullable=True)
    gas_fee = Column(Float, nullable=True)

    # Transaction metadata
    description = Column(Text, nullable=True)
    reference_id = Column(String(100), nullable=True)
    transaction_metadata = Column(Text, nullable=True)  # JSON string

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, type='{self.transaction_type.value}', amount={self.amount})>"
