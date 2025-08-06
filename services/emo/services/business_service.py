from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Dict, Any
import os
import uuid
from datetime import datetime

from config import settings
from models.business import Business, BusinessType, BusinessStatus, BusinessCategory
from models.company_profile import CompanyProfile, CompanySize, IndustryType


class BusinessService:
    """Service for managing business entities"""

    def __init__(self, db: Session):
        self.db = db

    def create_business(self, user_id: int, business_data: Dict[str, Any]) -> Business:
        """Create a new business entity"""
        business = Business(
            user_id=user_id,
            business_name=business_data["business_name"],
            business_type=business_data["business_type"],
            category=business_data["category"],
            email=business_data["email"],
            phone=business_data.get("phone"),
            website=business_data.get("website"),
            address_line1=business_data["address_line1"],
            address_line2=business_data.get("address_line2"),
            city=business_data["city"],
            state=business_data["state"],
            postal_code=business_data["postal_code"],
            country=business_data["country"],
            description=business_data.get("description"),
            registration_number=business_data.get("registration_number"),
            tax_id=business_data.get("tax_id"),
            annual_revenue=business_data.get("annual_revenue"),
            founded_date=business_data.get("founded_date"),
            status=BusinessStatus.PENDING,
        )

        self.db.add(business)
        self.db.commit()
        self.db.refresh(business)
        return business

    def get_business(self, business_id: int) -> Optional[Business]:
        """Get business by ID"""
        return self.db.query(Business).filter(Business.id == business_id).first()

    def get_user_businesses(self, user_id: int) -> List[Business]:
        """Get all businesses for a user"""
        return self.db.query(Business).filter(Business.user_id == user_id).all()

    def update_business(
        self, business_id: int, update_data: Dict[str, Any]
    ) -> Optional[Business]:
        """Update business information"""
        business = self.get_business(business_id)
        if not business:
            return None

        # Update fields
        for field, value in update_data.items():
            if hasattr(business, field) and value is not None:
                setattr(business, field, value)

        business.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(business)
        return business

    def verify_business(
        self, business_id: int, verification_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Verify business with external sources"""
        business = self.get_business(business_id)
        if not business:
            return {"error": "Business not found"}

        try:
            # Simulate external verification
            verification_result = self._verify_with_external_sources(business)

            # Update business with verification results
            business.verification_score = verification_result.get("score", 0.0)
            business.risk_score = verification_result.get("risk_score", 0.0)
            business.is_verified = verification_result.get("is_valid", False)
            business.verified_at = (
                datetime.utcnow()
                if verification_result.get("is_valid", False)
                else None
            )
            business.admin_notes = verification_result.get("notes", "")

            if verification_result.get("is_valid", False):
                business.status = BusinessStatus.VERIFIED
            else:
                business.status = BusinessStatus.REJECTED

            self.db.commit()
            self.db.refresh(business)

            return {
                "success": True,
                "business_id": business.id,
                "status": business.status.value,
                "verification_result": verification_result,
            }

        except Exception as e:
            return {"error": f"Verification failed: {str(e)}"}

    def _verify_with_external_sources(self, business: Business) -> Dict[str, Any]:
        """Verify business with external sources (simulated)"""
        # In a real implementation, this would call external APIs
        return {
            "is_valid": True,
            "score": 0.85,
            "risk_score": 0.15,
            "notes": "Business verified successfully",
            "external_checks": {
                "business_registry": True,
                "tax_authority": True,
                "regulatory_database": True,
                "fraud_check": False,
                "blacklist_check": False,
            },
        }

    def create_company_profile(
        self, business_id: int, profile_data: Dict[str, Any]
    ) -> CompanyProfile:
        """Create company profile for business"""
        profile = CompanyProfile(
            business_id=business_id,
            company_name=profile_data["company_name"],
            legal_name=profile_data.get("legal_name"),
            dba_name=profile_data.get("dba_name"),
            industry=profile_data["industry"],
            company_size=profile_data.get("company_size"),
            annual_revenue=profile_data.get("annual_revenue"),
            funding_stage=profile_data.get("funding_stage"),
            investors=profile_data.get("investors"),
            primary_contact_name=profile_data.get("primary_contact_name"),
            primary_contact_email=profile_data.get("primary_contact_email"),
            primary_contact_phone=profile_data.get("primary_contact_phone"),
            website=profile_data.get("website"),
            linkedin_url=profile_data.get("linkedin_url"),
            twitter_url=profile_data.get("twitter_url"),
            facebook_url=profile_data.get("facebook_url"),
            business_hours=profile_data.get("business_hours"),
            certifications=profile_data.get("certifications"),
            awards=profile_data.get("awards"),
            target_market=profile_data.get("target_market"),
            competitors=profile_data.get("competitors"),
            market_position=profile_data.get("market_position"),
        )

        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_company_profile(self, business_id: int) -> Optional[CompanyProfile]:
        """Get company profile for business"""
        return (
            self.db.query(CompanyProfile)
            .filter(CompanyProfile.business_id == business_id)
            .first()
        )

    def update_company_profile(
        self, business_id: int, update_data: Dict[str, Any]
    ) -> Optional[CompanyProfile]:
        """Update company profile"""
        profile = self.get_company_profile(business_id)
        if not profile:
            return None

        # Update fields
        for field, value in update_data.items():
            if hasattr(profile, field) and value is not None:
                setattr(profile, field, value)

        profile.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_business_statistics(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get business processing statistics"""
        query = self.db.query(Business)

        if user_id:
            query = query.filter(Business.user_id == user_id)

        total_businesses = query.count()
        pending_businesses = query.filter(
            Business.status == BusinessStatus.PENDING
        ).count()
        verified_businesses = query.filter(
            Business.status == BusinessStatus.VERIFIED
        ).count()
        rejected_businesses = query.filter(
            Business.status == BusinessStatus.REJECTED
        ).count()
        active_businesses = query.filter(Business.is_active == True).count()

        return {
            "total": total_businesses,
            "pending": pending_businesses,
            "verified": verified_businesses,
            "rejected": rejected_businesses,
            "active": active_businesses,
        }

    def delete_business(self, business_id: int) -> bool:
        """Delete a business"""
        business = self.get_business(business_id)
        if not business:
            return False

        self.db.delete(business)
        self.db.commit()
        return True
