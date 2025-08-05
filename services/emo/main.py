from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="EMO - Easy Management Office",
    description="EHB Easy Management Office API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class OfficeProfile(BaseModel):
    user_id: int
    office_name: str
    office_type: str
    verification_status: str
    business_license: str
    employee_count: int
    office_address: str
    contact_info: dict

class BusinessVerification(BaseModel):
    user_id: int
    business_name: str
    business_type: str
    license_number: str
    tax_id: str
    documents: List[str]

class VerificationResult(BaseModel):
    verification_id: str
    status: str
    score: int
    message: str
    timestamp: datetime

# Mock data
office_profiles = {
    1: {
        "user_id": 1,
        "office_name": "Tech Solutions Inc",
        "office_type": "technology",
        "verification_status": "verified",
        "business_license": "BL-2024-001",
        "employee_count": 25,
        "office_address": "123 Business St, Tech City",
        "contact_info": {
            "phone": "+1-555-0123",
            "email": "contact@techsolutions.com",
            "website": "www.techsolutions.com"
        }
    },
    2: {
        "user_id": 2,
        "office_name": "Green Energy Co",
        "office_type": "energy",
        "verification_status": "pending",
        "business_license": "BL-2024-002",
        "employee_count": 15,
        "office_address": "456 Green Ave, Eco City",
        "contact_info": {
            "phone": "+1-555-0456",
            "email": "info@greenenergy.com",
            "website": "www.greenenergy.com"
        }
    }
}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "EMO - Easy Management Office",
        "version": "1.0.0",
        "status": "running",
        "port": 4003
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "EMO",
        "timestamp": datetime.now()
    }

@app.get("/profile/{user_id}")
async def get_office_profile(user_id: int):
    """Get user's office profile"""
    if user_id not in office_profiles:
        raise HTTPException(status_code=404, detail="Office profile not found")

    return office_profiles[user_id]

@app.post("/verify-business")
async def verify_business(verification: BusinessVerification):
    """Verify business/office"""
    # Mock verification logic
    verification_id = f"EMO_{verification.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Simulate verification process
    if verification.business_type in ["technology", "consulting", "services"]:
        score = 90
        status = "verified"
        message = "Business verification successful"
    elif verification.business_type in ["energy", "manufacturing"]:
        score = 85
        status = "verified"
        message = "Business verification successful"
    else:
        score = 75
        status = "pending"
        message = "Business verification pending review"

    # Update office profile
    if verification.user_id in office_profiles:
        office_profiles[verification.user_id]["verification_status"] = status

    return VerificationResult(
        verification_id=verification_id,
        status=status,
        score=score,
        message=message,
        timestamp=datetime.now()
    )

@app.get("/business-stats/{user_id}")
async def get_business_stats(user_id: int):
    """Get business statistics"""
    if user_id not in office_profiles:
        raise HTTPException(status_code=404, detail="User not found")

    profile = office_profiles[user_id]

    # Mock business statistics
    stats = {
        "total_revenue": 150000,
        "monthly_growth": 12.5,
        "employee_satisfaction": 85,
        "customer_rating": 4.2,
        "projects_completed": 45,
        "active_projects": 8
    }

    return {
        "user_id": user_id,
        "office_name": profile["office_name"],
        "business_stats": stats,
        "last_updated": datetime.now()
    }

@app.post("/update-office/{user_id}")
async def update_office_profile(user_id: int, office_data: dict):
    """Update office profile"""
    if user_id not in office_profiles:
        raise HTTPException(status_code=404, detail="User not found")

    # Update profile with new data
    office_profiles[user_id].update(office_data)

    return {
        "user_id": user_id,
        "message": "Office profile updated successfully",
        "updated_at": datetime.now()
    }

@app.get("/office-directory")
async def get_office_directory():
    """Get directory of all verified offices"""
    verified_offices = [
        {
            "user_id": profile["user_id"],
            "office_name": profile["office_name"],
            "office_type": profile["office_type"],
            "location": profile["office_address"],
            "contact": profile["contact_info"]
        }
        for profile in office_profiles.values()
        if profile["verification_status"] == "verified"
    ]

    return {
        "total_offices": len(verified_offices),
        "offices": verified_offices
    }

@app.get("/verification-history/{user_id}")
async def get_verification_history(user_id: int):
    """Get office verification history"""
    if user_id not in office_profiles:
        raise HTTPException(status_code=404, detail="User not found")

    # Mock verification history
    history = [
        {
            "verification_id": f"EMO_{user_id}_001",
            "type": "business_license_verification",
            "status": "completed",
            "score": 95,
            "timestamp": datetime.now(),
            "method": "document_review"
        },
        {
            "verification_id": f"EMO_{user_id}_002",
            "type": "tax_id_verification",
            "status": "completed",
            "score": 90,
            "timestamp": datetime.now(),
            "method": "government_database"
        }
    ]

    return {
        "user_id": user_id,
        "verification_history": history,
        "total_verifications": len(history)
    }

@app.get("/office-types")
async def get_office_types():
    """Get available office types"""
    return {
        "office_types": [
            "technology",
            "consulting",
            "services",
            "energy",
            "manufacturing",
            "healthcare",
            "education",
            "finance",
            "retail",
            "other"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4003, reload=True)
