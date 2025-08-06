from datetime import datetime
from typing import List, Optional

from database.connection import get_db
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from models.business import Business, BusinessCreate, BusinessResponse, BusinessUpdate
from models.company_profile import (
    CompanyProfile,
    CompanyProfileCreate,
    CompanyProfileResponse,
    CompanyProfileUpdate,
)
from services.business_service import BusinessService
from sqlalchemy.orm import Session

router = APIRouter(prefix="/business", tags=["Business Management"])


@router.post("/", response_model=BusinessResponse)
async def create_business(
    business_data: BusinessCreate,
    db: Session = Depends(get_db)
):
    """Create a new business entity"""
    service = BusinessService(db)
    business = service.create_business(
        user_id=business_data.user_id,
        business_data=business_data.dict()
    )
    return business


@router.get("/{business_id}", response_model=BusinessResponse)
async def get_business(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get business by ID"""
    service = BusinessService(db)
    business = service.get_business(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business


@router.get("/user/{user_id}", response_model=List[BusinessResponse])
async def get_user_businesses(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all businesses for a user"""
    service = BusinessService(db)
    businesses = service.get_user_businesses(user_id)
    return businesses


@router.put("/{business_id}", response_model=BusinessResponse)
async def update_business(
    business_id: int,
    update_data: BusinessUpdate,
    db: Session = Depends(get_db)
):
    """Update business information"""
    service = BusinessService(db)
    business = service.update_business(business_id, update_data.dict(exclude_unset=True))
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business


@router.post("/{business_id}/verify")
async def verify_business(
    business_id: int,
    verification_data: dict,
    db: Session = Depends(get_db)
):
    """Verify business with external sources"""
    service = BusinessService(db)
    result = service.verify_business(business_id, verification_data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/{business_id}/profile", response_model=CompanyProfileResponse)
async def create_company_profile(
    business_id: int,
    profile_data: CompanyProfileCreate,
    db: Session = Depends(get_db)
):
    """Create company profile for business"""
    service = BusinessService(db)
    profile = service.create_company_profile(business_id, profile_data.dict())
    return profile


@router.get("/{business_id}/profile", response_model=CompanyProfileResponse)
async def get_company_profile(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get company profile for business"""
    service = BusinessService(db)
    profile = service.get_company_profile(business_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Company profile not found")
    return profile


@router.put("/{business_id}/profile", response_model=CompanyProfileResponse)
async def update_company_profile(
    business_id: int,
    update_data: CompanyProfileUpdate,
    db: Session = Depends(get_db)
):
    """Update company profile"""
    service = BusinessService(db)
    profile = service.update_company_profile(business_id, update_data.dict(exclude_unset=True))
    if not profile:
        raise HTTPException(status_code=404, detail="Company profile not found")
    return profile


@router.get("/statistics")
async def get_business_statistics(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get business processing statistics"""
    service = BusinessService(db)
    stats = service.get_business_statistics(user_id)
    return stats


@router.delete("/{business_id}")
async def delete_business(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Delete a business"""
    service = BusinessService(db)
    success = service.delete_business(business_id)
    if not success:
        raise HTTPException(status_code=404, detail="Business not found")
    return {"message": "Business deleted successfully"}
