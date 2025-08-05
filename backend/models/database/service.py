from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from .base import Base


class ServiceType(enum.Enum):
    PSS = "pss"  # KYC verification
    EMO = "emo"  # Business verification
    EDR = "edr"  # Skill testing
    JPS = "jps"  # Job profile
    GOSELLR = "gosellr"  # E-commerce
    WALLET = "wallet"  # Payments
    AI_AGENT = "ai_agent"  # AI services
    AI_ROBOT = "ai_robot"  # AI automation


class ServiceStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    DEPRECATED = "deprecated"


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(Enum(ServiceType), nullable=False)
    status = Column(Enum(ServiceStatus), default=ServiceStatus.ACTIVE)

    # Service configuration
    port = Column(Integer, nullable=False)
    host = Column(String(100), default="localhost")
    endpoint = Column(String(200))

    # Service metadata
    description = Column(Text)
    version = Column(String(20), default="1.0.0")
    documentation_url = Column(String(500))

    # Configuration
    config = Column(Text)  # JSON string for service configuration
    environment_vars = Column(Text)  # JSON string for environment variables

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_health_check = Column(DateTime(timezone=True))

    # Health monitoring
    is_healthy = Column(Boolean, default=True)
    response_time = Column(Integer)  # in milliseconds
    error_count = Column(Integer, default=0)

    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}', type='{self.type.value}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value if self.type else None,
            'status': self.status.value if self.status else None,
            'port': self.port,
            'host': self.host,
            'endpoint': self.endpoint,
            'description': self.description,
            'version': self.version,
            'documentation_url': self.documentation_url,
            'is_healthy': self.is_healthy,
            'response_time': self.response_time,
            'error_count': self.error_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None
        }


class UserService(Base):
    __tablename__ = "user_services"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    # Service access
    is_enabled = Column(Boolean, default=True)
    access_level = Column(String(50), default="basic")

    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime(timezone=True))

    # Settings
    settings = Column(Text)  # JSON string for user-specific settings

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User")
    service = relationship("Service")

    def __repr__(self):
        return f"<UserService(user_id={self.user_id}, service_id={self.service_id})>"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'service_id': self.service_id,
            'is_enabled': self.is_enabled,
            'access_level': self.access_level,
            'usage_count': self.usage_count,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
