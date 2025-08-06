from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum,
    Text,
    ForeignKey,
    Numeric,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from .base import Base


class TransactionType(enum.Enum):
    PAYMENT = "payment"
    REFUND = "refund"
    TRANSFER = "transfer"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    FEE = "fee"
    REWARD = "reward"


class TransactionStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethod(enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    CRYPTO = "crypto"
    EHBGC = "ehbgc"  # EHB Global Coin


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), unique=True, index=True, nullable=False)

    # User and service relationships
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)

    # Transaction details
    type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    payment_method = Column(Enum(PaymentMethod), nullable=True)

    # Amount and currency
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="USD")
    fee_amount = Column(Numeric(10, 2), default=0)
    net_amount = Column(Numeric(10, 2), nullable=False)

    # Transaction metadata
    description = Column(Text)
    reference = Column(String(200))
    external_id = Column(String(200))  # External payment provider ID

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))

    # Additional data
    transaction_metadata = Column(Text)  # JSON string for additional data
    error_message = Column(Text)

    # Relationships
    user = relationship("User")
    service = relationship("Service")

    def __repr__(self):
        return f"<Transaction(id={self.id}, transaction_id='{self.transaction_id}', amount={self.amount})>"

    def to_dict(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "service_id": self.service_id,
            "type": self.type.value if self.type else None,
            "status": self.status.value if self.status else None,
            "payment_method": (
                self.payment_method.value if self.payment_method else None
            ),
            "amount": float(self.amount) if self.amount else 0,
            "currency": self.currency,
            "fee_amount": float(self.fee_amount) if self.fee_amount else 0,
            "net_amount": float(self.net_amount) if self.net_amount else 0,
            "description": self.description,
            "reference": self.reference,
            "external_id": self.external_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "transaction_metadata": self.transaction_metadata,
            "error_message": self.error_message,
        }


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Balance information
    balance = Column(Numeric(10, 2), default=0)
    currency = Column(String(3), default="USD")

    # Wallet status
    is_active = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)

    # Security
    pin_hash = Column(String(255))
    two_factor_enabled = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_activity = Column(DateTime(timezone=True))

    # Settings
    settings = Column(Text)  # JSON string for wallet settings

    # Relationships
    user = relationship("User")

    def __repr__(self):
        return f"<Wallet(id={self.id}, user_id={self.user_id}, balance={self.balance})>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "balance": float(self.balance) if self.balance else 0,
            "currency": self.currency,
            "is_active": self.is_active,
            "is_locked": self.is_locked,
            "two_factor_enabled": self.two_factor_enabled,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_activity": (
                self.last_activity.isoformat() if self.last_activity else None
            ),
        }
