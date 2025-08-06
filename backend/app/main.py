from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

"""
EHB Main Application
FastAPI backend for EHB ecosystem
"""

# Load environment variables
load_dotenv()

# Mock data for services
mock_services = [
    {
        "id": "1",
        "name": "PSS - Personal Security System",
        "description": "Complete personal security and verification system",
        "type": "security",
        "status": "active",
        "version": "1.0.0",
        "port": 4001,
        "host": "localhost",
        "endpoint": "/api/pss",
        "documentation_url": "/docs/pss",
        "is_healthy": True,
        "response_time": 150,
        "error_count": 0,
        "created_at": "2025-01-01T00:00:00Z"
    },
    {
        "id": "2",
        "name": "EMO - EHB Management Organization",
        "description": "Business management and organization system",
        "type": "business",
        "status": "active",
        "version": "1.0.0",
        "port": 4003,
        "host": "localhost",
        "endpoint": "/api/emo",
        "documentation_url": "/docs/emo",
        "is_healthy": True,
        "response_time": 120,
        "error_count": 0,
        "created_at": "2025-01-01T00:00:00Z"
    },
    {
        "id": "3",
        "name": "EDR - EHB Digital Records",
        "description": "Digital record management system",
        "type": "records",
        "status": "pending",
        "version": "1.0.0",
        "port": 4002,
        "host": "localhost",
        "endpoint": "/api/edr",
        "documentation_url": "/docs/edr",
        "is_healthy": False,
        "response_time": 500,
        "error_count": 5,
        "created_at": "2025-01-01T00:00:00Z"
    }
]

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
    print("🚀 Starting EHB Main Application...")
    await initialize_services()
    yield
    # Shutdown
    print("🛑 Shutting down EHB Main Application...")
    await cleanup_services()


async def initialize_services():
    """Initialize all services"""
    print("📡 Initializing services...")
    # In a real implementation, this would check service health
    app_state["system_health"] = "healthy"


async def cleanup_services():
    """Cleanup services on shutdown"""
    print("🧹 Cleaning up services...")
    app_state["system_health"] = "shutdown"


# Create FastAPI app
app = FastAPI(
    title="EHB Home Page API",
    description="Main API for EHB ecosystem services",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Response models
class ServiceResponse(BaseModel):
    id: str
    name: str
    description: str
    type: str
    status: str
    version: str
    port: int
    host: str
    endpoint: str
    documentation_url: str
    is_healthy: bool
    response_time: int
    error_count: int
    created_at: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    sql_level: str
    sql_points: int
    sql_rank: str
    status: str
    is_verified: bool
    is_admin: bool
    verification_progress: int
    created_at: str

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


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        services=app_state["services"],
        database="connected"
    )


@app.get("/api/services", response_model=List[ServiceResponse])
async def get_services_endpoint(
    category: Optional[str] = Query(None, description="Filter by service category"),
    status: Optional[str] = Query(None, description="Filter by service status")
):
    """Get all services with optional filtering"""
    services = mock_services.copy()

    if category:
        services = [s for s in services if s["type"] == category]

    if status:
        services = [s for s in services if s["status"] == status]

    return services


@app.get("/api/services/{service_id}", response_model=ServiceResponse)
async def get_service_endpoint(service_id: str):
    """Get specific service by ID"""
    service = next((s for s in mock_services if s["id"] == service_id), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@app.get("/api/services/featured", response_model=List[ServiceResponse])
async def get_featured_services_endpoint():
    """Get featured services"""
    featured_services = [
        s for s in mock_services
        if s["status"] == "active" and s["is_healthy"]
    ]
    return featured_services[:3]  # Return top 3 featured services


@app.get("/api/search", response_model=SearchResponse)
async def search_endpoint(
    q: str = Query(..., description="Search query")
):
    """Search services and users"""
    # Mock search implementation
    matching_services = [
        s for s in mock_services
        if q.lower() in s["name"].lower() or q.lower() in s["description"].lower()
    ]

    # Mock users
    mock_users = [
        UserResponse(
            id="1",
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
            sql_level="expert",
            sql_points=1500,
            sql_rank="gold",
            status="active",
            is_verified=True,
            is_admin=False,
            verification_progress=100,
            created_at="2025-01-01T00:00:00Z"
        )
    ]

    return SearchResponse(
        services=matching_services,
        users=mock_users,
        total_results=len(matching_services) + len(mock_users)
    )


@app.get("/api/users", response_model=List[UserResponse])
async def get_users_endpoint(
    sql_level: Optional[str] = Query(None, description="Filter by SQL level"),
    status: Optional[str] = Query(None, description="Filter by user status")
):
    """Get all users with optional filtering"""
    # Mock users data
    mock_users = [
        UserResponse(
            id="1",
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
            sql_level="expert",
            sql_points=1500,
            sql_rank="gold",
            status="active",
            is_verified=True,
            is_admin=False,
            verification_progress=100,
            created_at="2025-01-01T00:00:00Z"
        )
    ]
    return mock_users


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user_endpoint(user_id: str):
    """Get specific user by ID"""
    # Mock user data
    return UserResponse(
        id=user_id,
        username="john_doe",
        email="john@example.com",
        full_name="John Doe",
        sql_level="expert",
        sql_points=1500,
        sql_rank="gold",
        status="active",
        is_verified=True,
        is_admin=False,
        verification_progress=100,
        created_at="2025-01-01T00:00:00Z"
    )


@app.get("/api/stats/overview")
async def get_overview_stats():
    """Get overview statistics"""
    return {
        "total_users": app_state["active_users"],
        "total_services": len(app_state["services"]),
        "active_services": len([s for s in app_state["services"].values() if s["status"] == "ready"]),
        "system_health": app_state["system_health"]
    }


@app.get("/api/dashboard/services")
async def get_services_dashboard():
    """Get services dashboard data"""
    return {
        "services": app_state["services"],
        "total_services": len(app_state["services"]),
        "healthy_services": len([s for s in app_state["services"].values() if s["status"] == "ready"])
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to EHB Home Page API",
        "version": "1.0.0",
        "status": "running",
        "services": len(app_state["services"]),
        "active_users": app_state["active_users"]
    }


@app.get("/api")
async def api_info():
    """API information"""
    return {
        "name": "EHB Home Page API",
        "version": "1.0.0",
        "description": "Main API for EHB ecosystem services",
        "endpoints": {
            "health": "/health",
            "services": "/api/services",
            "users": "/api/users",
            "search": "/api/search",
            "stats": "/api/stats/overview",
            "dashboard": "/api/dashboard/services"
        },
        "documentation": "/docs"
    }


@app.get("/api/sql/{user_id}")
async def get_sql_level_endpoint(user_id: str):
    """Get SQL level for a user"""
    # Mock SQL level data
    return {
        "user_id": user_id,
        "sql_level": "expert",
        "sql_points": 1500,
        "sql_rank": "gold",
        "progress": 85,
        "next_level": "master",
        "points_needed": 200
    }


@app.get("/api/services/status")
async def get_services_status():
    """Get services status"""
    return app_state["services"]


@app.get("/api/dashboard")
async def get_dashboard_data():
    """Get comprehensive dashboard data"""
    return {
        "user_stats": {
            "total_users": app_state["active_users"],
            "active_users": 890,
            "new_users_today": 45,
            "verified_users": 1200
        },
        "service_stats": {
            "total_services": len(app_state["services"]),
            "active_services": len([s for s in app_state["services"].values() if s["status"] == "ready"]),
            "services_with_errors": len([s for s in app_state["services"].values() if s["status"] == "error"])
        },
        "system_stats": {
            "uptime": "99.9%",
            "response_time": "150ms",
            "error_rate": "0.1%",
            "last_backup": "2025-01-01T00:00:00Z"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
