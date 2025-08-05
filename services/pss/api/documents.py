from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import uuid
from datetime import datetime

from backend.models.database.connection import get_db
from backend.services.auth.auth import get_current_user
from backend.models.database.user import User
from models.kyc_document import (
    KYCDocument, DocumentType, DocumentStatus,
    DocumentUploadRequest, DocumentResponse, DocumentUpdateRequest
)
from services.document_service import DocumentService
from config import settings

router = APIRouter(prefix="/documents", tags=["documents"])

# Initialize document service
document_service = DocumentService()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: DocumentType = Form(...),
    document_number: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a KYC document"""
    try:
        # Validate file
        if not document_service.validate_file(file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type or size"
            )

        # Save document
        document = await document_service.save_document(
            db=db,
            user_id=current_user.id,
            file=file,
            document_type=document_type,
            document_number=document_number
        )

        return DocumentResponse.from_orm(document)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document upload failed: {str(e)}"
        )


@router.get("/", response_model=List[DocumentResponse])
async def get_user_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all documents for current user"""
    documents = document_service.get_user_documents(db, current_user.id)
    return [DocumentResponse.from_orm(doc) for doc in documents]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific document"""
    document = document_service.get_document(db, document_id, current_user.id)

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return DocumentResponse.from_orm(document)


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: int,
    update_data: DocumentUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update document information"""
    document = document_service.update_document(
        db, document_id, current_user.id, update_data.dict()
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return DocumentResponse.from_orm(document)


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete document"""
    success = document_service.delete_document(db, document_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return {"message": "Document deleted successfully"}


@router.post("/{document_id}/process")
async def process_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Process document with OCR"""
    try:
        result = await document_service.process_document(db, document_id, current_user.id)
        return {
            "message": "Document processing started",
            "document_id": document_id,
            "status": "processing"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document processing failed: {str(e)}"
        )


@router.get("/{document_id}/ocr")
async def get_document_ocr(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get OCR results for document"""
    ocr_data = document_service.get_document_ocr(db, document_id, current_user.id)

    if not ocr_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="OCR data not found"
        )

    return ocr_data


# Admin endpoints
@router.get("/admin/all", response_model=List[DocumentResponse])
async def get_all_documents(
    status: Optional[DocumentStatus] = None,
    document_type: Optional[DocumentType] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all documents (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    documents = document_service.get_all_documents(db, status, document_type)
    return [DocumentResponse.from_orm(doc) for doc in documents]


@router.put("/admin/{document_id}/approve")
async def approve_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Approve document (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    success = document_service.approve_document(db, document_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return {"message": "Document approved successfully"}


@router.put("/admin/{document_id}/reject")
async def reject_document(
    document_id: int,
    reason: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject document (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    success = document_service.reject_document(db, document_id, reason, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return {"message": "Document rejected successfully"}
