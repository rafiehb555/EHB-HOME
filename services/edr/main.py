from contextlib import asynccontextmanager

import uvicorn
from config import settings
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from models import Assessment, Course, Progress, Quiz

from api import assessments, courses, progress, quizzes
from backend.models.database.connection import create_tables
from backend.services.auth.auth import get_current_user

# Import API routers
# Security scheme
security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print(f"🚀 Starting {settings.SERVICE_NAME} v{settings.SERVICE_VERSION}")
    print(f"📊 Database: {settings.DATABASE_URL}")
    print(f"🔐 Port: {settings.PORT}")

    # Create database tables
    try:
        create_tables()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Database setup failed: {e}")

    yield

    # Shutdown
    print(f"🛑 Shutting down {settings.SERVICE_NAME}")


# Create FastAPI app
app = FastAPI(
    title=settings.SERVICE_NAME,
    version=settings.SERVICE_VERSION,
    description="EDR Service - Skill Testing & Assessment System",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(courses.router, prefix="/api/v1", tags=["courses"])
app.include_router(assessments.router, prefix="/api/v1", tags=["assessments"])
app.include_router(quizzes.router, prefix="/api/v1", tags=["quizzes"])
app.include_router(progress.router, prefix="/api/v1", tags=["progress"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.SERVICE_NAME,
        "version": settings.SERVICE_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": settings.SERVICE_VERSION,
    }


@app.get("/api/v1/status")
async def service_status(current_user=Depends(get_current_user)):
    """Get service status (requires authentication)"""
    return {
        "service": settings.SERVICE_NAME,
        "version": settings.SERVICE_VERSION,
        "status": "operational",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
        },
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
