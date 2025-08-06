import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import aiofiles
from config import settings
from models.kyc_document import DocumentStatus, DocumentType, KYCDocument
from models.verification import Verification, VerificationStatus
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session


class DocumentService:
    """Service for managing KYC documents"""

    def __init__(self, db: Session):
        self.db = db

    def create_document(
        self,
        user_id: int,
        document_type: DocumentType,
        file_path: str,
        metadata: Optional[Dict] = None,
    ) -> KYCDocument:
        """Create a new KYC document"""
        document = KYCDocument(
            user_id=user_id,
            document_type=document_type,
            file_path=file_path,
            status=DocumentStatus.PENDING,
            metadata=metadata or {},
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_document(self, document_id: int) -> Optional[KYCDocument]:
        """Get document by ID"""
        return self.db.query(KYCDocument).filter(KYCDocument.id == document_id).first()

    def get_user_documents(self, user_id: int) -> List[KYCDocument]:
        """Get all documents for a user"""
        return self.db.query(KYCDocument).filter(KYCDocument.user_id == user_id).all()

    def update_document_status(
        self,
        document_id: int,
        status: DocumentStatus,
        admin_notes: Optional[str] = None,
    ) -> Optional[KYCDocument]:
        """Update document status"""
        document = self.get_document(document_id)
        if not document:
            return None

        document.status = status
        document.admin_notes = admin_notes
        document.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(document)
        return document

    def process_document(self, document_id: int) -> Dict[str, Any]:
        """Process document for OCR and validation"""
        document = self.get_document(document_id)
        if not document:
            return {"error": "Document not found"}

        try:
            # Simulate OCR processing
            ocr_result = self._perform_ocr(document.file_path)

            # Update document with OCR results
            document.metadata.update(
                {
                    "ocr_result": ocr_result,
                    "processed_at": datetime.utcnow().isoformat(),
                }
            )

            # Update status based on OCR results
            if ocr_result.get("confidence", 0) > 0.8:
                document.status = DocumentStatus.PROCESSED
            else:
                document.status = DocumentStatus.REJECTED

            self.db.commit()
            self.db.refresh(document)

            return {
                "success": True,
                "document_id": document.id,
                "status": document.status.value,
                "ocr_result": ocr_result,
            }

        except Exception as e:
            return {"error": f"Processing failed: {str(e)}"}

    def _perform_ocr(self, file_path: str) -> Dict[str, Any]:
        """Perform OCR on document (simulated)"""
        # In a real implementation, this would use OCR libraries
        # For now, we'll simulate the process
        return {
            "confidence": 0.85,
            "text": "Simulated OCR text",
            "fields": {
                "name": "John Doe",
                "date_of_birth": "1990-01-01",
                "document_number": "123456789",
            },
        }

    def validate_document(self, document_id: int) -> Dict[str, Any]:
        """Validate document against external databases"""
        document = self.get_document(document_id)
        if not document:
            return {"error": "Document not found"}

        try:
            # Simulate external validation
            validation_result = self._validate_with_external_sources(document)

            # Update document with validation results
            document.metadata.update(
                {
                    "validation_result": validation_result,
                    "validated_at": datetime.utcnow().isoformat(),
                }
            )

            if validation_result.get("is_valid", False):
                document.status = DocumentStatus.VERIFIED
            else:
                document.status = DocumentStatus.REJECTED

            self.db.commit()
            self.db.refresh(document)

            return {
                "success": True,
                "document_id": document.id,
                "status": document.status.value,
                "validation_result": validation_result,
            }

        except Exception as e:
            return {"error": f"Validation failed: {str(e)}"}

    def _validate_with_external_sources(self, document: KYCDocument) -> Dict[str, Any]:
        """Validate document with external sources (simulated)"""
        # In a real implementation, this would call external APIs
        return {
            "is_valid": True,
            "confidence": 0.9,
            "external_checks": {
                "government_database": True,
                "fraud_check": False,
                "blacklist_check": False,
            },
        }

    def get_document_statistics(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get document processing statistics"""
        query = self.db.query(KYCDocument)

        if user_id:
            query = query.filter(KYCDocument.user_id == user_id)

        total_documents = query.count()
        pending_documents = query.filter(
            KYCDocument.status == DocumentStatus.PENDING
        ).count()
        processed_documents = query.filter(
            KYCDocument.status == DocumentStatus.PROCESSED
        ).count()
        verified_documents = query.filter(
            KYCDocument.status == DocumentStatus.VERIFIED
        ).count()
        rejected_documents = query.filter(
            KYCDocument.status == DocumentStatus.REJECTED
        ).count()

        return {
            "total": total_documents,
            "pending": pending_documents,
            "processed": processed_documents,
            "verified": verified_documents,
            "rejected": rejected_documents,
        }

    def delete_document(self, document_id: int) -> bool:
        """Delete a document"""
        document = self.get_document(document_id)
        if not document:
            return False

        # Delete file from storage
        if os.path.exists(document.file_path):
            os.remove(document.file_path)

        self.db.delete(document)
        self.db.commit()
        return True
