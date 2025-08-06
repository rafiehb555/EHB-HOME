from contextlib import asynccontextmanager

import uvicorn
from config import settings
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from models import Marketplace, Order, Product, Seller

from api import marketplace, orders, products, sellers
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
    description="GoSellr Service - E-commerce & Marketplace Platform",
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
app.include_router(products.router, prefix="/api/v1", tags=["products"])
app.include_router(orders.router, prefix="/api/v1", tags=["orders"])
app.include_router(sellers.router, prefix="/api/v1", tags=["sellers"])
app.include_router(marketplace.router, prefix="/api/v1", tags=["marketplace"])


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
