import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from models.business import Business, BusinessStatus
from sqlalchemy.orm import Session


class VerificationService:
    """Service for managing business verification workflows"""

    def __init__(self, db: Session):
        self.db = db



    def initiate_verification(self, business_id: int) -> Dict[str, Any]:
        """Initiate verification process for a business"""
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return {"error": "Business not found"}

        try:
            # Create verification record
            verification_id = str(uuid.uuid4())

            # Update business status
            business.status = BusinessStatus.PENDING
            business.verification_started_at = datetime.utcnow()
            business.metadata = business.metadata or {}
            business.metadata["verification_id"] = verification_id

            self.db.commit()

            return {
                "success": True,
                "business_id": business.id,
                "verification_id": verification_id,
                "status": "verification_initiated",
                "estimated_completion": "3-5 business days"
            }

        except Exception as e:
            return {"error": f"Verification initiation failed: {str(e)}"}

    def perform_verification_checks(self, business_id: int) -> Dict[str, Any]:
        """Perform comprehensive verification checks"""
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return {"error": "Business not found"}

        try:
            # Simulate verification checks
            checks = {
                "business_registry": self._check_business_registry(business),
                "tax_authority": self._check_tax_authority(business),
                "regulatory_database": self._check_regulatory_database(business),
                "fraud_detection": self._check_fraud_detection(business),
                "blacklist_check": self._check_blacklist(business),
                "address_verification": self._check_address_verification(business),
                "contact_verification": self._check_contact_verification(business)
            }

            # Calculate overall score
            passed_checks = sum(1 for check in checks.values() if check.get("passed", False))
            total_checks = len(checks)
            verification_score = (passed_checks / total_checks) * 100

            # Determine verification result
            is_verified = verification_score >= 80.0
            risk_score = 100 - verification_score

            # Update business with verification results
            business.verification_score = verification_score
            business.risk_score = risk_score
            business.is_verified = is_verified
            business.verification_completed_at = datetime.utcnow()
            business.metadata["verification_checks"] = checks
            business.metadata["verification_score"] = verification_score

            if is_verified:
                business.status = BusinessStatus.VERIFIED
                business.verified_at = datetime.utcnow()
            else:
                business.status = BusinessStatus.REJECTED

            self.db.commit()

            return {
                "success": True,
                "business_id": business.id,
                "verification_score": verification_score,
                "risk_score": risk_score,
                "is_verified": is_verified,
                "checks": checks,
                "status": business.status.value
            }

        except Exception as e:
            return {"error": f"Verification checks failed: {str(e)}"}

    def _check_business_registry(self, business: Business) -> Dict[str, Any]:
        """Check business registry (simulated)"""
        return {
            "passed": True,
            "score": 0.9,
            "details": "Business found in official registry",
            "timestamp": datetime.utcnow().isoformat()
        }

    def _check_tax_authority(self, business: Business) -> Dict[str, Any]:
        """Check tax authority records (simulated)"""
        return {
            "passed": True,
            "score": 0.85,
            "details": "Tax ID verified with authority",
            "timestamp": datetime.utcnow().isoformat()
        }

    def _check_regulatory_database(self, business: Business) -> Dict[str, Any]:
        """Check regulatory compliance (simulated)"""
        return {
            "passed": True,
            "score": 0.95,
            "details": "No regulatory violations found",
            "timestamp": datetime.utcnow().isoformat()
        }

    def _check_fraud_detection(self, business: Business) -> Dict[str, Any]:
        """Check for fraud indicators (simulated)"""
        return {
            "passed": True,
            "score": 0.88,
            "details": "No fraud indicators detected",
            "timestamp": datetime.utcnow().isoformat()
        }

    def _check_blacklist(self, business: Business) -> Dict[str, Any]:
        """Check against blacklists (simulated)"""
        return {
            "passed": True,
            "score": 1.0,
            "details": "Not found in any blacklists",
            "timestamp": datetime.utcnow().isoformat()
        }

    def _check_address_verification(self, business: Business) -> Dict[str, Any]:
        """Verify business address (simulated)"""
        return {
            "passed": True,
            "score": 0.92,
            "details": "Address verified with postal service",
            "timestamp": datetime.utcnow().isoformat()
        }

    def _check_contact_verification(self, business: Business) -> Dict[str, Any]:
        """Verify contact information (simulated)"""
        return {
            "passed": True,
            "score": 0.87,
            "details": "Contact information verified",
            "timestamp": datetime.utcnow().isoformat()
        }

    def get_verification_status(self, business_id: int) -> Dict[str, Any]:
        """Get current verification status"""
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return {"error": "Business not found"}

        return {
            "business_id": business.id,
            "status": business.status.value,
            "verification_score": business.verification_score,
            "risk_score": business.risk_score,
            "is_verified": business.is_verified,
            "verification_started_at": business.verification_started_at.isoformat() if business.verification_started_at else None,
            "verification_completed_at": business.verification_completed_at.isoformat() if business.verification_completed_at else None,
            "verified_at": business.verified_at.isoformat() if business.verified_at else None
        }

    def request_review(self, business_id: int, review_reason: str) -> Dict[str, Any]:
        """Request manual review for verification"""
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return {"error": "Business not found"}

        try:
            business.status = BusinessStatus.UNDER_REVIEW
            business.admin_notes = review_reason
            business.updated_at = datetime.utcnow()

            self.db.commit()

            return {
                "success": True,
                "business_id": business.id,
                "status": "under_review",
                "review_reason": review_reason
            }

        except Exception as e:
            return {"error": f"Review request failed: {str(e)}"}

    def approve_verification(self, business_id: int, admin_notes: str = None) -> Dict[str, Any]:
        """Approve business verification (admin action)"""
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return {"error": "Business not found"}

        try:
            business.status = BusinessStatus.VERIFIED
            business.is_verified = True
            business.verified_at = datetime.utcnow()
            business.admin_notes = admin_notes
            business.updated_at = datetime.utcnow()

            self.db.commit()

            return {
                "success": True,
                "business_id": business.id,
                "status": "verified",
                "verified_at": business.verified_at.isoformat()
            }

        except Exception as e:
            return {"error": f"Approval failed: {str(e)}"}

    def reject_verification(self, business_id: int, rejection_reason: str) -> Dict[str, Any]:
        """Reject business verification (admin action)"""
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return {"error": "Business not found"}

        try:
            business.status = BusinessStatus.REJECTED
            business.is_verified = False
            business.admin_notes = rejection_reason
            business.updated_at = datetime.utcnow()

            self.db.commit()

            return {
                "success": True,
                "business_id": business.id,
                "status": "rejected",
                "rejection_reason": rejection_reason
            }

        except Exception as e:
            return {"error": f"Rejection failed: {str(e)}"}
