import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Service Configuration
    SERVICE_NAME: str = "EDR Service"
    SERVICE_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 4002

    # Database Configuration
    DATABASE_URL: str = "postgresql://ehb_user:ehb_password@localhost:5432/ehb_database"

    # JWT Configuration
    SECRET_KEY: str = "ehb-edr-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # File Upload Configuration
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: list = [
        ".jpg",
        ".jpeg",
        ".png",
        ".pdf",
        ".doc",
        ".docx",
        ".mp4",
        ".avi",
        ".mov",
    ]

    # Content Management
    CONTENT_STORAGE_PATH: str = "content"
    VIDEO_STORAGE_PATH: str = "videos"
    DOCUMENT_STORAGE_PATH: str = "documents"

    # Assessment Configuration
    QUIZ_TIME_LIMIT: int = 60  # minutes
    MAX_ATTEMPTS_PER_QUIZ: int = 3
    PASSING_SCORE: float = 70.0  # percentage

    # Redis Configuration (for Celery)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # Security Configuration
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    RATE_LIMIT_PER_MINUTE: int = 60

    # Analytics Configuration
    ANALYTICS_ENABLED: bool = True
    PROGRESS_TRACKING_INTERVAL: int = 5  # minutes

    # Notification Configuration
    EMAIL_NOTIFICATIONS: bool = True
    SMS_NOTIFICATIONS: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Ensure upload directory exists


def ensure_upload_dir():
    """Ensure upload directory exists"""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "courses"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "assessments"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "content"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "temp"), exist_ok=True)


# Initialize upload directory
ensure_upload_dir()
