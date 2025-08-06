import asyncio
from datetime import datetime
from typing import Dict, List, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException
from models.database.user import User
from pydantic import BaseModel

from services.auth.auth import get_current_user

router = APIRouter(prefix="/services", tags=["services"])

# Service configurations
SERVICES = {
    "pss": {"url": "http://localhost:4001", "name": "Personal Security System"},
    "emo": {"url": "http://localhost:4003", "name": "Easy Management Office"},
    "edr": {"url": "http://localhost:4002", "name": "Exam Decision Registration"},
    "jps": {"url": "http://localhost:4005", "name": "Job Profile System"},
    "gosellr": {"url": "http://localhost:4004", "name": "GoSellr Marketplace"},
    "wallet": {"url": "http://localhost:5001", "name": "EHB Wallet"},
    "ai-agent": {"url": "http://localhost:4007", "name": "AI Agent"},
    "ai-robot": {"url": "http://localhost:4008", "name": "AI Robot"},
}


class ServiceStatus(BaseModel):
    service: str
    status: str
    response_time: float
    last_check: datetime
    url: str


class ServiceHealth(BaseModel):
    service: str
    healthy: bool
    message: str
    timestamp: datetime


async def check_service_health(service_name: str, service_url: str) -> ServiceHealth:
    """Check health of a specific service"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            start_time = datetime.now()
            response = await client.get(f"{service_url}/health")
            response_time = (datetime.now() - start_time).total_seconds()

            if response.status_code == 200:
                return ServiceHealth(
                    service=service_name,
                    healthy=True,
                    message="Service is healthy",
                    timestamp=datetime.now(),
                )
            else:
                return ServiceHealth(
                    service=service_name,
                    healthy=False,
                    message=f"Service returned status {response.status_code}",
                    timestamp=datetime.now(),
                )
    except Exception as e:
        return ServiceHealth(
            service=service_name,
            healthy=False,
            message=f"Service unreachable: {str(e)}",
            timestamp=datetime.now(),
        )


@router.get("/health")
async def get_all_services_health():
    """Get health status of all services"""
    health_checks = []

    for service_name, service_config in SERVICES.items():
        health = await check_service_health(service_name, service_config["url"])
        health_checks.append(health)

    healthy_count = sum(1 for h in health_checks if h.healthy)
    total_count = len(health_checks)

    return {
        "total_services": total_count,
        "healthy_services": healthy_count,
        "unhealthy_services": total_count - healthy_count,
        "services": health_checks,
        "overall_status": "healthy" if healthy_count == total_count else "degraded",
    }


@router.get("/{service_name}/health")
async def get_service_health(service_name: str):
    """Get health status of a specific service"""
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    service_config = SERVICES[service_name]
    health = await check_service_health(service_name, service_config["url"])

    return health


@router.get("/{service_name}/profile/{user_id}")
async def get_service_profile(
    service_name: str, user_id: int, current_user: User = Depends(get_current_user)
):
    """Get user profile from specific service"""
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    service_config = SERVICES[service_name]

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{service_config['url']}/profile/{user_id}")

            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code, detail="Service error"
                )

    except Exception as e:
        raise HTTPException(
            status_code=503, detail=f"Service {service_name} is unavailable"
        )


@router.post("/{service_name}/verify")
async def verify_with_service(
    service_name: str,
    verification_data: dict,
    current_user: User = Depends(get_current_user),
):
    """Submit verification to specific service"""
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    service_config = SERVICES[service_name]

    # Add user_id to verification data
    verification_data["user_id"] = current_user.id

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            if service_name == "pss":
                response = await client.post(
                    f"{service_config['url']}/verify", json=verification_data
                )
            elif service_name == "emo":
                response = await client.post(
                    f"{service_config['url']}/verify-business", json=verification_data
                )
            elif service_name == "edr":
                response = await client.post(
                    f"{service_config['url']}/register-exam", json=verification_data
                )
            else:
                raise HTTPException(
                    status_code=400, detail="Service does not support verification"
                )

            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(
                    status_code=response.status_code, detail="Service error"
                )

    except Exception as e:
        raise HTTPException(
            status_code=503, detail=f"Service {service_name} is unavailable"
        )


@router.get("/user/{user_id}/verification-status")
async def get_user_verification_status(
    user_id: int, current_user: User = Depends(get_current_user)
):
    """Get user's verification status across all services"""
    verification_status = {}

    for service_name, service_config in SERVICES.items():
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(
                    f"{service_config['url']}/profile/{user_id}"
                )

                if response.status_code == 200:
                    data = response.json()
                    verification_status[service_name] = {
                        "status": data.get("verification_status", "unknown"),
                        "score": data.get("security_score", data.get("score", 0)),
                        "last_updated": datetime.now(),
                    }
                else:
                    verification_status[service_name] = {
                        "status": "error",
                        "score": 0,
                        "last_updated": datetime.now(),
                    }

        except Exception:
            verification_status[service_name] = {
                "status": "unavailable",
                "score": 0,
                "last_updated": datetime.now(),
            }

    # Calculate overall verification progress
    verified_services = sum(
        1 for status in verification_status.values() if status["status"] == "verified"
    )
    total_services = len(verification_status)
    progress_percentage = (
        (verified_services / total_services) * 100 if total_services > 0 else 0
    )

    return {
        "user_id": user_id,
        "verification_status": verification_status,
        "overall_progress": progress_percentage,
        "verified_services": verified_services,
        "total_services": total_services,
    }


@router.get("/available-services")
async def get_available_services():
    """Get list of all available services"""
    return {
        "services": [
            {
                "name": service_name,
                "display_name": config["name"],
                "url": config["url"],
                "description": f"EHB {config['name']} service",
            }
            for service_name, config in SERVICES.items()
        ]
    }
