import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Service Configuration
    SERVICE_NAME: str = "PSS Service"
    SERVICE_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 4001

    # Database Configuration
    DATABASE_URL: str = "postgresql://ehb_user:ehb_password@localhost:5432/ehb_database"

    # JWT Configuration
    SECRET_KEY: str = "ehb-pss-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Upload Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: list = [".jpg", ".jpeg", ".png", ".pdf"]

    # OCR Configuration
    TESSERACT_CMD: str = "tesseract"
    OCR_LANGUAGES: str = "eng"

    # External APIs
    OCR_API_URL: Optional[str] = None
    ADDRESS_VERIFICATION_API: Optional[str] = None
    RISK_ASSESSMENT_API: Optional[str] = None

    # Redis Configuration (for Celery)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Security Configuration
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    RATE_LIMIT_PER_MINUTE: int = 60

    # Compliance Configuration
    COMPLIANCE_CHECK_INTERVAL: int = 24  # hours
    RISK_THRESHOLD: float = 0.7

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Ensure upload directory exists


def ensure_upload_dir():
    """Ensure upload directory exists"""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "documents"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "temp"), exist_ok=True)


# Initialize upload directory
ensure_upload_dir()
