"""
EHB Main Application
FastAPI backend for EHB ecosystem with MongoDB
"""

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv

# Import MongoDB utilities
from utils.database.mongodb import (
    connect_to_mongodb,
    close_mongodb_connection,
    initialize_database,
    test_mongodb_connection,
    get_services,
    get_service,
    get_user,
    get_user_by_email,
    create_user,
    create_service,
    get_transactions
)

# Import auth routes
from api.v1.auth import router as auth_router
from api.v1.services import router as services_router

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

    # Test MongoDB connection
    if await test_mongodb_connection():
        print("✅ MongoDB connection successful")
        # Initialize database with sample data
        await initialize_database()
    else:
        print("❌ MongoDB connection failed")

    # Initialize services
    await initialize_services()

    yield

    # Shutdown
    print("🛑 Shutting down EHB Home Page & Dashboard...")
    await close_mongodb_connection()
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
        timestamp=datetime.now(),
        services=app_state["services"],
        database="MongoDB"
    )


@app.get("/api/services", response_model=List[ServiceResponse])
async def get_services_endpoint(
    category: Optional[str] = Query(None, description="Filter by service category"),
    status: Optional[str] = Query(None, description="Filter by service status")
):
    """Get all services with optional filtering"""
    try:
        services = await get_services()

        # Apply filters
        if category:
            services = [s for s in services if s.get("type") == category]
        if status:
            services = [s for s in services if s.get("status") == status]

        # Convert to response format
        response_services = []
        for service in services:
            response_services.append(ServiceResponse(
                id=str(service["_id"]),
                name=service["name"],
                description=service["description"],
                type=service["type"],
                status=service["status"],
                version=service["version"],
                port=service["port"],
                host=service["host"],
                endpoint=service["endpoint"],
                documentation_url=service["documentation_url"],
                is_healthy=service["is_healthy"],
                response_time=service["response_time"],
                error_count=service["error_count"],
                created_at=service["created_at"]
            ))

        return response_services
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/services/{service_id}", response_model=ServiceResponse)
async def get_service_endpoint(service_id: str):
    """Get a specific service by ID"""
    service = await get_service(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return ServiceResponse(
        id=str(service["_id"]),
        name=service["name"],
        description=service["description"],
        type=service["type"],
        status=service["status"],
        version=service["version"],
        port=service["port"],
        host=service["host"],
        endpoint=service["endpoint"],
        documentation_url=service["documentation_url"],
        is_healthy=service["is_healthy"],
        response_time=service["response_time"],
        error_count=service["error_count"],
        created_at=service["created_at"]
    )


@app.get("/api/services/featured", response_model=List[ServiceResponse])
async def get_featured_services_endpoint():
    """Get featured services"""
    try:
        services = await get_services()
        featured_services = [s for s in services if s.get("status") == "active"][:5]

        response_services = []
        for service in featured_services:
            response_services.append(ServiceResponse(
                id=str(service["_id"]),
                name=service["name"],
                description=service["description"],
                type=service["type"],
                status=service["status"],
                version=service["version"],
                port=service["port"],
                host=service["host"],
                endpoint=service["endpoint"],
                documentation_url=service["documentation_url"],
                is_healthy=service["is_healthy"],
                response_time=service["response_time"],
                error_count=service["error_count"],
                created_at=service["created_at"]
            ))

        return response_services
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/search", response_model=SearchResponse)
async def search_endpoint(
    q: str = Query(..., description="Search query")
):
    """Search services and users"""
    try:
        # Search services
        services = await get_services()
        matching_services = [
            s for s in services
            if q.lower() in s["name"].lower() or q.lower() in s["description"].lower()
        ]

        # Search users (simplified for now)
        users = []  # TODO: Implement user search

        # Convert services to response format
        response_services = []
        for service in matching_services:
            response_services.append(ServiceResponse(
                id=str(service["_id"]),
                name=service["name"],
                description=service["description"],
                type=service["type"],
                status=service["status"],
                version=service["version"],
                port=service["port"],
                host=service["host"],
                endpoint=service["endpoint"],
                documentation_url=service["documentation_url"],
                is_healthy=service["is_healthy"],
                response_time=service["response_time"],
                error_count=service["error_count"],
                created_at=service["created_at"]
            ))

        return SearchResponse(
            services=response_services,
            users=[],  # TODO: Convert users to UserResponse
            total_results=len(response_services) + len(users)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@app.get("/api/users", response_model=List[UserResponse])
async def get_users_endpoint(
    sql_level: Optional[str] = Query(None, description="Filter by SQL level"),
    status: Optional[str] = Query(None, description="Filter by user status")
):
    """Get all users with optional filtering"""
    try:
        # TODO: Implement user listing with filters
        # For now, return empty list
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user_endpoint(user_id: str):
    """Get a specific user by ID"""
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"],
        full_name=user["full_name"],
        sql_level=user["sql_level"],
        sql_points=user["sql_points"],
        sql_rank=user["sql_rank"],
        status=user["status"],
        is_verified=user["is_verified"],
        is_admin=user["is_admin"],
        verification_progress=user["verification_progress"],
        created_at=user["created_at"]
    )


@app.get("/api/stats/overview")
async def get_overview_stats():
    """Get overview statistics"""
    try:
        services = await get_services()
        total_services = len(services)
        active_services = len([s for s in services if s.get("status") == "active"])

        return {
            "total_users": 2,  # TODO: Get from database
            "total_services": total_services,
            "active_services": active_services,
            "system_health": app_state["system_health"],
            "active_users": app_state["active_users"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")


@app.get("/api/dashboard/services")
async def get_services_dashboard():
    """Get services for dashboard"""
    try:
        services = await get_services()
        return {
            "services": services,
            "total_count": len(services),
            "healthy_count": len([s for s in services if s.get("is_healthy")])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "EHB Home Page & Dashboard API",
        "version": "1.0.0",
        "status": "running",
        "database": "MongoDB"
    }


@app.get("/api")
async def api_info():
    """API information"""
    return {
        "name": "EHB Home Page & Dashboard API",
        "version": "1.0.0",
        "description": "Complete EHB ecosystem with all services",
        "endpoints": {
            "health": "/health",
            "services": "/api/services",
            "users": "/api/users",
            "search": "/api/search",
            "dashboard": "/api/dashboard/services"
        }
    }


@app.get("/api/sql/{user_id}")
async def get_sql_level_endpoint(user_id: str):
    """Get SQL level for a user"""
    try:
        user = await get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "user_id": user_id,
            "sql_level": user["sql_level"],
            "sql_points": user["sql_points"],
            "sql_rank": user["sql_rank"],
            "verification_progress": user["verification_progress"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL level error: {str(e)}")


@app.get("/api/services/status")
async def get_services_status():
    """Get status of all services"""
    return app_state["services"]


@app.get("/api/dashboard")
async def get_dashboard_data():
    """Get dashboard data"""
    try:
        services = await get_services()
        total_services = len(services)

        return {
            "overview": {
                "total_users": 2,  # TODO: Get from database
                "total_services": total_services,
                "active_users": app_state["active_users"]
            },
            "services": app_state["services"],
            "system_health": app_state["system_health"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard data error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
