import enum

from sqlalchemy import (Boolean, Column, DateTime, Enum, Float, Integer,
                        String, Text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

"""
Service Model for EHB System
"""


class ServiceType(enum.Enum):
    """Service types"""

    PSS = "pss"
    EMO = "emo"
    EDR = "edr"
    JPS = "jps"
    GOSELLR = "gosellr"
    WALLET = "wallet"
    FRANCHISE = "franchise"
    AI_MARKETPLACE = "ai_marketplace"
    AI_AGENT = "ai_agent"
    AI_ROBOT = "ai_robot"


class ServiceStatus(enum.Enum):
    """Service status"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    DEPRECATED = "deprecated"


class Service(Base):
    """Service model for EHB system"""

    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    service_type = Column(Enum(ServiceType), nullable=False)
    status = Column(Enum(ServiceStatus), default=ServiceStatus.ACTIVE)

    # Service configuration
    description = Column(Text, nullable=True)
    version = Column(String(20), default="1.0.0")
    endpoint_url = Column(String(255), nullable=True)
    api_key_required = Column(Boolean, default=False)

    # Pricing and limits
    price_per_month = Column(Float, default=0.0)
    usage_limit = Column(Integer, default=1000)
    current_usage = Column(Integer, default=0)

    # Service metadata
    icon_url = Column(String(255), nullable=True)
    documentation_url = Column(String(255), nullable=True)
    support_email = Column(String(100), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_maintenance = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}', type='{self.service_type.value}')>"
