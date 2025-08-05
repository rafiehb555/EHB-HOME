"""
Wallet Model for EHB System
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from .base import Base


class WalletType(enum.Enum):
    """Wallet types"""
    HOT = "hot"
    COLD = "cold"
    MULTISIG = "multisig"


class WalletStatus(enum.Enum):
    """Wallet status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOCKED = "locked"
    PENDING = "pending"


class Wallet(Base):
    """Wallet model for EHB system"""
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    wallet_type = Column(Enum(WalletType), default=WalletType.HOT)
    status = Column(Enum(WalletStatus), default=WalletStatus.ACTIVE)

    # Wallet addresses
    ethereum_address = Column(String(255), unique=True, index=True, nullable=True)
    polygon_address = Column(String(255), unique=True, index=True, nullable=True)
    bsc_address = Column(String(255), unique=True, index=True, nullable=True)

    # Balances
    usd_balance = Column(Float, default=0.0)
    eth_balance = Column(Float, default=0.0)
    bnb_balance = Column(Float, default=0.0)
    matic_balance = Column(Float, default=0.0)
    ehbgc_balance = Column(Float, default=0.0)

    # Security
    is_encrypted = Column(Boolean, default=True)
    encryption_key_hash = Column(String(255), nullable=True)
    backup_phrase_hash = Column(String(255), nullable=True)

    # Metadata
    wallet_name = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_sync = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="wallets")

    def __repr__(self):
        return f"<Wallet(id={self.id}, user_id={self.user_id}, type='{self.wallet_type.value}')>"
