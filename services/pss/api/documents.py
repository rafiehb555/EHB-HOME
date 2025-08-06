import os
import uuid
from datetime import datetime
from typing import List, Optional

from config import settings
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from models.kyc_document import (DocumentResponse, DocumentService,
                                 DocumentStatus, DocumentType,
                                 DocumentUpdateRequest, DocumentUploadRequest,
                                 KYCDocument, Session,
                                 backend.models.database.connection,
                                 backend.services.auth.auth, from,
                                 get_current_user, get_db, import, json,
                                 services.document_service, sqlalchemy.orm)

router = APIRouter()


@router.post("/documents/upload", response_model=DocumentResponse)
async def upload_document(
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Upload a KYC document"""
    try:
        # Validate file type
        if not file.filename.lower().endswith(tuple(settings.ALLOWED_EXTENSIONS)):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Allowed: " + ", ".join(settings.ALLOWED_EXTENSIONS)
            )

        # Create unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Parse metadata
        metadata_dict = {}
        if metadata:
            try:
                metadata_dict = json.loads(metadata)
            except:
                metadata_dict = {"original_filename": file.filename}
        else:
            metadata_dict = {"original_filename": file.filename}

        # Create document record
        document_service = DocumentService(db)
        document = document_service.create_document(
            user_id=current_user.id,
            document_type=document_type,
            file_path=file_path,
            metadata=metadata_dict
        )

        return DocumentResponse.from_orm(document)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get document by ID"""
    document_service = DocumentService(db)
    document = document_service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Check if user has access to this document
    if document.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    return DocumentResponse.from_orm(document)


@router.get("/documents/user/{user_id}", response_model=List[DocumentResponse])
async def get_user_documents(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all documents for a user"""
    # Check if user has access
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    document_service = DocumentService(db)
    documents = document_service.get_user_documents(user_id)

    return [DocumentResponse.from_orm(doc) for doc in documents]


@router.put("/documents/{document_id}/status", response_model=DocumentResponse)
async def update_document_status(
    document_id: int,
    status: DocumentStatus,
    admin_notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update document status (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    document_service = DocumentService(db)
    document = document_service.update_document_status(document_id, status, admin_notes)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return DocumentResponse.from_orm(document)


@router.post("/documents/{document_id}/process")
async def process_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Process document for OCR and validation"""
    document_service = DocumentService(db)
    result = document_service.process_document(document_id)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/documents/{document_id}/validate")
async def validate_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Validate document against external databases"""
    document_service = DocumentService(db)
    result = document_service.validate_document(document_id)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.get("/documents/statistics")
async def get_document_statistics(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get document processing statistics"""
    # Check if user has access
    if user_id and user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    document_service = DocumentService(db)
    stats = document_service.get_document_statistics(user_id)

    return stats


@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete a document"""
    document_service = DocumentService(db)
    document = document_service.get_document(document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Check if user has access
    if document.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    success = document_service.delete_document(document_id)

    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete document")

    return {"message": "Document deleted successfully"}


@router.get("/documents/admin/all", response_model=List[DocumentResponse])
async def get_all_documents(
    skip: int = 0,
    limit: int = 100,
    status: Optional[DocumentStatus] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all documents (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    query = db.query(KYCDocument)

    if status:
        query = query.filter(KYCDocument.status == status)

    documents = query.offset(skip).limit(limit).all()

    return [DocumentResponse.from_orm(doc) for doc in documents]
