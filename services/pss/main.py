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
    title="PSS - Personal Security System",
    description="EHB Personal Security System API",
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
class SecurityProfile(BaseModel):
    user_id: int
    security_level: str
    verification_status: str
    last_verification: Optional[datetime]
    security_score: int
    risk_level: str

class VerificationRequest(BaseModel):
    user_id: int
    document_type: str
    document_data: str
    verification_method: str

class VerificationResponse(BaseModel):
    verification_id: str
    status: str
    score: int
    message: str
    timestamp: datetime

# Mock data
security_profiles = {
    1: {
        "user_id": 1,
        "security_level": "high",
        "verification_status": "verified",
        "last_verification": datetime.now(),
        "security_score": 95,
        "risk_level": "low"
    },
    2: {
        "user_id": 2,
        "security_level": "medium",
        "verification_status": "pending",
        "last_verification": None,
        "security_score": 65,
        "risk_level": "medium"
    }
}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "PSS - Personal Security System",
        "version": "1.0.0",
        "status": "running",
        "port": 4001
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "PSS",
        "timestamp": datetime.now()
    }

@app.get("/profile/{user_id}")
async def get_security_profile(user_id: int):
    """Get user's security profile"""
    if user_id not in security_profiles:
        raise HTTPException(status_code=404, detail="Security profile not found")

    return security_profiles[user_id]

@app.post("/verify")
async def verify_user(verification: VerificationRequest):
    """Verify user identity"""
    # Mock verification logic
    verification_id = f"PSS_{verification.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Simulate verification process
    if verification.document_type == "id_card":
        score = 90
        status = "verified"
        message = "Identity verification successful"
    elif verification.document_type == "passport":
        score = 95
        status = "verified"
        message = "Passport verification successful"
    else:
        score = 70
        status = "pending"
        message = "Document verification pending review"

    # Update security profile
    if verification.user_id in security_profiles:
        security_profiles[verification.user_id]["verification_status"] = status
        security_profiles[verification.user_id]["security_score"] = score
        security_profiles[verification.user_id]["last_verification"] = datetime.now()

    return VerificationResponse(
        verification_id=verification_id,
        status=status,
        score=score,
        message=message,
        timestamp=datetime.now()
    )

@app.get("/risk-assessment/{user_id}")
async def get_risk_assessment(user_id: int):
    """Get user's risk assessment"""
    if user_id not in security_profiles:
        raise HTTPException(status_code=404, detail="User not found")

    profile = security_profiles[user_id]

    # Mock risk assessment
    risk_factors = {
        "verification_status": profile["verification_status"],
        "security_score": profile["security_score"],
        "account_age": "30 days",
        "login_patterns": "normal",
        "suspicious_activity": False
    }

    return {
        "user_id": user_id,
        "risk_level": profile["risk_level"],
        "risk_score": 100 - profile["security_score"],
        "risk_factors": risk_factors,
        "recommendations": [
            "Enable two-factor authentication",
            "Update security questions",
            "Review login history"
        ]
    }

@app.post("/update-security-level/{user_id}")
async def update_security_level(user_id: int, security_level: str):
    """Update user's security level"""
    if user_id not in security_profiles:
        raise HTTPException(status_code=404, detail="User not found")

    if security_level not in ["low", "medium", "high", "maximum"]:
        raise HTTPException(status_code=400, detail="Invalid security level")

    security_profiles[user_id]["security_level"] = security_level

    return {
        "user_id": user_id,
        "security_level": security_level,
        "updated_at": datetime.now()
    }

@app.get("/verification-history/{user_id}")
async def get_verification_history(user_id: int):
    """Get user's verification history"""
    if user_id not in security_profiles:
        raise HTTPException(status_code=404, detail="User not found")

    # Mock verification history
    history = [
        {
            "verification_id": f"PSS_{user_id}_001",
            "type": "identity_verification",
            "status": "completed",
            "score": 95,
            "timestamp": datetime.now(),
            "method": "document_upload"
        },
        {
            "verification_id": f"PSS_{user_id}_002",
            "type": "biometric_verification",
            "status": "completed",
            "score": 98,
            "timestamp": datetime.now(),
            "method": "fingerprint"
        }
    ]

    return {
        "user_id": user_id,
        "verification_history": history,
        "total_verifications": len(history)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4001, reload=True)
