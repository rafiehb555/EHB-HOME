import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Service Configuration
    SERVICE_NAME: str = "GoSellr Service"
    SERVICE_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 4004

    # Database Configuration
    DATABASE_URL: str = "postgresql://ehb_user:ehb_password@localhost:5432/ehb_database"

    # JWT Configuration
    SECRET_KEY: str = "ehb-gosellr-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Upload Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".jpg", ".jpeg", ".png", ".gif", ".webp"]

    # Product Management
    PRODUCT_IMAGES_PATH: str = "products"
    CATEGORY_IMAGES_PATH: str = "categories"
    MAX_PRODUCT_IMAGES: int = 10

    # Payment Configuration
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    PAYPAL_CLIENT_ID: Optional[str] = None
    PAYPAL_CLIENT_SECRET: Optional[str] = None

    # Marketplace Configuration
    COMMISSION_RATE: float = 0.05  # 5% commission
    MIN_ORDER_AMOUNT: float = 10.0
    MAX_ORDER_AMOUNT: float = 10000.0

    # Shipping Configuration
    DEFAULT_SHIPPING_COST: float = 5.99
    FREE_SHIPPING_THRESHOLD: float = 50.0
    SHIPPING_PROVIDERS: list = ["standard", "express", "overnight"]

    # Inventory Configuration
    LOW_STOCK_THRESHOLD: int = 5
    OUT_OF_STOCK_THRESHOLD: int = 0
    AUTO_RESTOCK_ENABLED: bool = True

    # Redis Configuration (for Celery)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Security Configuration
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    RATE_LIMIT_PER_MINUTE: int = 60

    # Notification Configuration
    EMAIL_NOTIFICATIONS: bool = True
    SMS_NOTIFICATIONS: bool = False
    PUSH_NOTIFICATIONS: bool = True

    # Analytics Configuration
    ANALYTICS_ENABLED: bool = True
    SALES_REPORTING_INTERVAL: int = 24  # hours

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Ensure upload directory exists


def ensure_upload_dir():
    """Ensure upload directory exists"""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "products"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "categories"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "sellers"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "temp"), exist_ok=True)


# Initialize upload directory
ensure_upload_dir()
