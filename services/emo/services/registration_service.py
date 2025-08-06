import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from config import settings
from models.business import Business, BusinessCategory, BusinessStatus, BusinessType
from models.company_profile import CompanyProfile, CompanySize, IndustryType
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session


class RegistrationService:
    """Service for managing business registration workflows"""

    def __init__(self, db: Session):
        self.db = db



    def start_registration(self, user_id: int, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new business registration process"""
        try:
            # Create initial business record
            business = Business(
                user_id=user_id,
                business_name=initial_data["business_name"],
                business_type=initial_data["business_type"],
                category=initial_data["category"],
                email=initial_data["email"],
                status=BusinessStatus.PENDING
            )

            self.db.add(business)
            self.db.commit()
            self.db.refresh(business)

            return {
                "success": True,
                "business_id": business.id,
                "registration_id": str(uuid.uuid4()),
                "status": "started",
                "next_steps": ["complete_profile", "upload_documents", "verification"]
            }

        except Exception as e:
            return {"error": f"Registration failed: {str(e)}"}

    def complete_profile(self, business_id: int, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete business profile information"""
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return {"error": "Business not found"}

        try:
            # Update business with complete information
            for field, value in profile_data.items():
                if hasattr(business, field) and value is not None:
                    setattr(business, field, value)

            business.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(business)

            return {
                "success": True,
                "business_id": business.id,
                "status": "profile_completed",
                "next_steps": ["upload_documents", "verification"]
            }

        except Exception as e:
            return {"error": f"Profile completion failed: {str(e)}"}

    def upload_documents(self, business_id: int, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Upload required documents for registration"""
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return {"error": "Business not found"}

        try:
            # Simulate document upload and processing
            uploaded_docs = []
            for doc in documents:
                doc_info = {
                    "document_type": doc["type"],
                    "file_name": doc["file_name"],
                    "uploaded_at": datetime.utcnow().isoformat(),
                    "status": "uploaded"
                }
                uploaded_docs.append(doc_info)

            # Update business with document information
            business.metadata = business.metadata or {}
            business.metadata["documents"] = uploaded_docs
            business.updated_at = datetime.utcnow()
            self.db.commit()

            return {
                "success": True,
                "business_id": business.id,
                "documents_uploaded": len(uploaded_docs),
                "status": "documents_uploaded",
                "next_steps": ["verification"]
            }

        except Exception as e:
            return {"error": f"Document upload failed: {str(e)}"}

    def submit_for_verification(self, business_id: int) -> Dict[str, Any]:
        """Submit business for verification"""
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return {"error": "Business not found"}

        try:
            # Check if all required information is complete
            if not self._is_registration_complete(business):
                return {"error": "Registration incomplete. Please complete all required fields."}

            # Update status to pending verification
            business.status = BusinessStatus.PENDING
            business.submitted_at = datetime.utcnow()
            self.db.commit()

            return {
                "success": True,
                "business_id": business.id,
                "status": "submitted_for_verification",
                "estimated_processing_time": "3-5 business days"
            }

        except Exception as e:
            return {"error": f"Submission failed: {str(e)}"}

    def _is_registration_complete(self, business: Business) -> bool:
        """Check if business registration is complete"""
        required_fields = [
            "business_name", "business_type", "category", "email",
            "address_line1", "city", "state", "postal_code", "country"
        ]

        for field in required_fields:
            if not getattr(business, field):
                return False

        return True


    def get_registration_status(self, business_id: int) -> Dict[str, Any]:
        """Get current registration status"""
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return {"error": "Business not found"}

        return {
            "business_id": business.id,
            "status": business.status.value,
            "progress": self._calculate_progress(business),
            "next_steps": self._get_next_steps(business),
            "last_updated": business.updated_at.isoformat() if business.updated_at else None
        }

    def _calculate_progress(self, business: Business) -> int:
        """Calculate registration progress percentage"""
        completed_steps = 0
        total_steps = 4

        # Basic info
        if business.business_name and business.email:
            completed_steps += 1

        # Profile completion
        if business.address_line1 and business.city:
            completed_steps += 1

        # Documents
        if business.metadata and business.metadata.get("documents"):
            completed_steps += 1

        # Submission
        if business.submitted_at:
            completed_steps += 1

        return int((completed_steps / total_steps) * 100)

    def _get_next_steps(self, business: Business) -> List[str]:
        """Get next steps for registration"""
        steps = []

        if not business.business_name or not business.email:
            steps.append("complete_basic_info")

        if not business.address_line1 or not business.city:
            steps.append("complete_address")

        if not business.metadata or not business.metadata.get("documents"):
            steps.append("upload_documents")

        if not business.submitted_at:
            steps.append("submit_for_verification")

        return steps


    def cancel_registration(self, business_id: int) -> Dict[str, Any]:
        """Cancel business registration"""
        business = self.db.query(Business).filter(Business.id == business_id).first()
        if not business:
            return {"error": "Business not found"}

        try:
            business.status = BusinessStatus.CANCELLED
            business.updated_at = datetime.utcnow()
            self.db.commit()

            return {
                "success": True,
                "business_id": business.id,
                "status": "cancelled"
            }

        except Exception as e:
            return {"error": f"Cancellation failed: {str(e)}"}
