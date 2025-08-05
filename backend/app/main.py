"""
EHB Main Application
FastAPI backend for EHB ecosystem
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import os

# Import models and database
from models.base import get_db, SessionLocal
from models.service import Service, ServiceType, ServiceStatus
from models.user import User, UserLevel, UserStatus
from models.transaction import Transaction
from models.wallet import Wallet
from models.franchise import Franchise
from models.verification import Verification

# Import Pydantic schemas
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Import database utilities
from utils.database.connection import get_db, create_tables, test_connection
from sqlalchemy.orm import Session

# Import models
from models.database.user import User
from models.database.service import Service, ServiceLog
from models.database.transaction import Transaction, Wallet

# Import auth routes
from api.v1.auth import router as auth_router
from api.v1.services import router as services_router

# Import contextlib and uvicorn
from contextlib import asynccontextmanager
import uvicorn
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Application state
app_state = {
    "services": {
        "pss": {"status": "ready", "port": 4001, "users": 890},
        "emo": {"status": "ready", "port": 4003, "users": 234},
        "edr": {"status": "pending", "port": 4002, "users": 156},
        "jps": {"status": "ready", "port": 4005, "users": 678},
        "gosellr": {"status": "ready", "port": 4004, "users": 450},
        "wallet": {"status": "ready", "port": 5001, "users": 320},
        "ai-agent": {"status": "ready", "port": 4007, "users": 89},
        "ai-robot": {"status": "error", "port": 4008, "users": 12}
    },
    "active_users": 1250,
    "system_health": "healthy"
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting EHB Home Page & Dashboard...")

    # Test database connection
    if test_connection():
        print("✅ Database connection successful")
        # Create tables if they don't exist
        create_tables()
    else:
        print("❌ Database connection failed")

    # Initialize services
    await initialize_services()

    yield

    # Shutdown
    print("🛑 Shutting down EHB Home Page & Dashboard...")
    await cleanup_services()


async def initialize_services():
    """Initialize all EHB services"""
    print("🔧 Initializing EHB services...")
    # This would connect to individual services
    # For now, we'll use mocked data


async def cleanup_services():
    """Cleanup services on shutdown"""
    print("🧹 Cleaning up services...")


# Create FastAPI app
app = FastAPI(
    title="EHB Home Page & Dashboard",
    description="Complete EHB ecosystem with all services",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(services_router, prefix="/api/v1")


# Pydantic schemas
class ServiceResponse(BaseModel):
    id: int
    name: str
    description: str
    service_type: str
    status: str
    version: str
    price_per_month: float
    usage_limit: int
    endpoint_url: str
    icon_url: str
    documentation_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    sql_level: str
    status: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

class SearchResponse(BaseModel):
    services: List[ServiceResponse]
    users: List[UserResponse]
    total_results: int

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    services: dict
    database: str

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        database_status = "connected"
    except Exception:
        database_status = "disconnected"

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        services={
            "frontend": "running",
            "backend": "running",
            "database": database_status
        },
        database=database_status
    )

# Services endpoints
@app.get("/api/services", response_model=List[ServiceResponse])
async def get_services(
    category: Optional[str] = Query(None, description="Filter by service category"),
    status: Optional[str] = Query(None, description="Filter by service status"),
    db: Session = Depends(get_db)
):
    """Get all services with optional filtering"""
    query = db.query(Service)

    if category:
        query = query.filter(Service.service_type == category)

    if status:
        query = query.filter(Service.status == status)

    services = query.all()
    return services

@app.get("/api/services/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    """Get a specific service by ID"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@app.get("/api/services/featured", response_model=List[ServiceResponse])
async def get_featured_services(db: Session = Depends(get_db)):
    """Get featured services"""
    services = db.query(Service).filter(Service.status == ServiceStatus.ACTIVE).limit(5).all()
    return services

# Search endpoint
@app.get("/api/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., description="Search query"),
    db: Session = Depends(get_db)
):
    """Search for services and users"""
    # Search services
    services = db.query(Service).filter(
        Service.name.ilike(f"%{q}%") |
        Service.description.ilike(f"%{q}%")
    ).limit(10).all()

    # Search users
    users = db.query(User).filter(
        User.username.ilike(f"%{q}%") |
        User.email.ilike(f"%{q}%")
    ).limit(10).all()

    total_results = len(services) + len(users)

    return SearchResponse(
        services=services,
        users=users,
        total_results=total_results
    )

# User endpoints
@app.get("/api/users", response_model=List[UserResponse])
async def get_users(
    sql_level: Optional[str] = Query(None, description="Filter by SQL level"),
    status: Optional[str] = Query(None, description="Filter by user status"),
    db: Session = Depends(get_db)
):
    """Get all users with optional filtering"""
    query = db.query(User)

    if sql_level:
        query = query.filter(User.sql_level == sql_level)

    if status:
        query = query.filter(User.status == status)

    users = query.all()
    return users

@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Statistics endpoints
@app.get("/api/stats/overview")
async def get_overview_stats(db: Session = Depends(get_db)):
    """Get overview statistics"""
    total_users = db.query(User).count()
    total_services = db.query(Service).count()
    total_transactions = db.query(Transaction).count()
    total_wallets = db.query(Wallet).count()

    active_services = db.query(Service).filter(Service.status == ServiceStatus.ACTIVE).count()
    verified_users = db.query(User).filter(User.is_verified == True).count()

    return {
        "users": {
            "total": total_users,
            "verified": verified_users,
            "active": total_users  # Simplified for now
        },
        "services": {
            "total": total_services,
            "active": active_services
        },
        "transactions": {
            "total": total_transactions
        },
        "wallets": {
            "total": total_wallets
        }
    }

# Dashboard endpoints
@app.get("/api/dashboard/services")
async def get_services_dashboard(db: Session = Depends(get_db)):
    """Get services dashboard data"""
    services = db.query(Service).all()

    service_stats = {}
    for service in services:
        service_stats[service.service_type.value] = {
            "name": service.name,
            "status": service.status.value,
            "price": service.price_per_month,
            "users": 0  # Placeholder for now
        }

    return {
        "services": service_stats,
        "total_services": len(services),
        "active_services": len([s for s in services if s.status == ServiceStatus.ACTIVE])
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "EHB API is running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# API info endpoint
@app.get("/api")
async def api_info():
    """API information"""
    return {
        "name": "EHB API",
        "version": "1.0.0",
        "description": "EHB Home Page and Services API",
        "endpoints": {
            "health": "/health",
            "services": "/api/services",
            "users": "/api/users",
            "search": "/api/search",
            "stats": "/api/stats/overview",
            "dashboard": "/api/dashboard/services"
        }
    }

# New endpoints from new_code
@app.get("/")
async def root():
    """Root endpoint with system overview"""
    return {
        "message": "EHB Home Page & Dashboard API",
        "version": "1.0.0",
        "status": "running",
        "services_count": len(app_state["services"]),
        "active_users": app_state["active_users"],
        "system_health": app_state["system_health"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if test_connection() else "disconnected",
        "services": len(app_state["services"])
    }


@app.get("/api/sql/{user_id}")
async def get_sql_level(user_id: int, db: Session = Depends(get_db)):
    """Get user's SQL level"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return {
                "user_id": user_id,
                "sql_level": user.sql_level.value,
                "sql_points": user.sql_points,
                "sql_rank": user.sql_rank,
                "verification_progress": user.verification_progress
            }
        else:
            return {
                "user_id": user_id,
                "sql_level": "Basic",
                "sql_points": 0,
                "sql_rank": "New User",
                "verification_progress": 0
            }
    except Exception as e:
        return {
            "user_id": user_id,
            "sql_level": "Basic",
            "sql_points": 0,
            "sql_rank": "New User",
            "verification_progress": 0,
            "error": str(e)
        }


@app.get("/api/services/status")
async def get_services_status():
    """Get status of all EHB services"""
    return {
        "services": app_state["services"],
        "total_services": len(app_state["services"]),
        "healthy_services": len([s for s in app_state["services"].values() if s["status"] == "ready"]),
        "system_health": app_state["system_health"]
    }


@app.get("/api/dashboard")
async def get_dashboard_data(db: Session = Depends(get_db)):
    """Get dashboard data"""
    try:
        # Get user statistics
        total_users = db.query(User).count()
        active_users = db.query(User).filter(User.status.value == "active").count()

        # Get service statistics
        total_services = db.query(Service).count()
        healthy_services = db.query(Service).filter(Service.is_healthy == True).count()

        # Get transaction statistics
        total_transactions = db.query(Transaction).count()
        completed_transactions = db.query(Transaction).filter(Transaction.status.value == "completed").count()

        return {
            "users": {
                "total": total_users,
                "active": active_users,
                "new_today": 45  # Mock data
            },
            "services": {
                "total": total_services,
                "healthy": healthy_services,
                "uptime": "99.9%"
            },
            "transactions": {
                "total": total_transactions,
                "completed": completed_transactions,
                "revenue_today": 12500  # Mock data
            },
            "system": {
                "health": "healthy",
                "last_update": "2024-01-20T10:30:00Z"
            }
        }
    except Exception as e:
        # Return mock data if database fails
        return {
            "users": {
                "total": 1250,
                "active": 890,
                "new_today": 45
            },
            "services": {
                "total": 8,
                "healthy": 7,
                "uptime": "99.9%"
            },
            "transactions": {
                "total": 156,
                "completed": 142,
                "revenue_today": 12500
            },
            "system": {
                "health": "healthy",
                "last_update": "2024-01-20T10:30:00Z"
            }
        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
