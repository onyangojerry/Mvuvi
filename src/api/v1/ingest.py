"""Newspaper ingestion endpoints for processing uploaded images."""

from datetime import datetime
from typing import Optional
from uuid import uuid4
import json

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status, Depends
from pydantic import BaseModel, Field

from src.config import get_settings
from src.services.storage_service import get_storage
from src.database import get_db
from src.models import OCRJob
from src.services import pubsub
from src.worker.celery_app import celery_app
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi import WebSocket
from src.ws.redis_ws import ws_manager

settings = get_settings()
router = APIRouter()


class IngestionResponse(BaseModel):
    """Response model for ingestion endpoint."""
    
    status: str = Field(description="Status of the ingestion")
    data: dict = Field(description="Ingestion data")
    meta: dict = Field(description="Metadata about the request")


class IngestionStatusResponse(BaseModel):
    """Response model for ingestion status check."""
    
    status: str = Field(description="Processing status")
    data: dict = Field(description="Processing data")


@router.post("/upload", response_model=IngestionResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_newspaper(
    image: UploadFile = File(..., description="Newspaper image (PNG, JPG, or PDF)"),
    language: Optional[str] = Form(default="en", description="Language code (e.g., 'en', 'es', 'fr')"),
    source: Optional[str] = Form(default=None, description="Newspaper source name"),
    db: AsyncSession = Depends(get_db),
    user_id: Optional[str] = None,  # TODO: Replace with actual user extraction from auth
):
    """
    Upload a newspaper image for OCR processing and text extraction.
    
    This endpoint accepts newspaper images and queues them for processing:
    - OCR text extraction
    - Neural network error correction
    - Content indexing
    - Feed integration
    
    **Supported formats**: PNG, JPG, JPEG, PDF
    **Max size**: 10MB
    **Processing time**: ~3-5 seconds
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "application/pdf"]
    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_IMAGE_FORMAT",
                "message": f"Unsupported file type: {image.content_type}",
                "details": {
                    "received_format": image.content_type,
                    "supported_formats": allowed_types,
                },
            },
        )
    
    # Validate file size
    contents = await image.read()
    file_size = len(contents)
    if file_size > settings.max_upload_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "code": "IMAGE_TOO_LARGE",
                "message": f"File size exceeds limit of {settings.max_image_size_mb}MB",
                "details": {
                    "file_size_bytes": file_size,
                    "max_size_bytes": settings.max_upload_size_bytes,
                },
            },
        )
    
    # Generate unique ID for this ingestion
    ingestion_id = str(uuid4())
    
    # Save file to storage (local by default)
    storage = get_storage()
    # rewind and save file
    try:
        await image.seek(0)
    except Exception:
        pass
    saved = await storage.save(image, user_id=user_id)
    if not saved or not saved.get("filename"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "UPLOAD_FAILED",
                "message": "Failed to save uploaded file.",
            },
        )

# Admin endpoint to trigger cleanup of old files
@router.post("/cleanup-uploads")
async def cleanup_uploads():
    storage = get_storage()
    storage.cleanup_old_files()
    return {"status": "success", "message": "Old files cleaned up."}

    # Persist an OCR job record
    job = OCRJob(
        filename=saved.get("filename"),
        engine=settings.ocr_engine,
        status="pending",
        file_size_kb=int(saved.get("size_bytes", 0) / 1024),
    )
    db.add(job)
    await db.flush()
    job_id = job.id

    # Prepare notification payload
    payload = {
        "event": "ocr_job_created",
        "job_id": job_id,
        "ingestion_id": ingestion_id,
        "filename": saved.get("filename"),
        "storage_path": saved.get("storage_path"),
        "created_at": datetime.utcnow().isoformat(),
    }

    # Publish notification (async, best-effort)
    try:
        await pubsub.publish_event(settings.redis_notifications_channel, payload)
    except Exception:
        pass

    # Enqueue OCR Celery task (fire-and-forget)
    try:
        celery_app.send_task(
            "src.tasks.ocr.process_ocr",
            args=[saved.get("storage_path"), ingestion_id, job_id, language],
            kwargs={},
        )
    except Exception:
        # If enqueue fails, we still return accepted but mark job as failed asynchronously
        pass

    return IngestionResponse(
        status="accepted",
        data={
            "id": ingestion_id,
            "type": "newspaper-upload",
            "attributes": {
                "filename": saved.get("filename"),
                "content_type": saved.get("content_type"),
                "file_size_bytes": saved.get("size_bytes"),
                "language": language,
                "source": source,
                "processing_status": "queued",
                "storage_path": saved.get("storage_path"),
                "job_id": job_id,
            },
        },
        meta={
            "timestamp": datetime.utcnow().isoformat(),
            "estimated_processing_time_seconds": 5,
        },
    )


@router.get("/status/{ingestion_id}", response_model=IngestionStatusResponse)
async def get_ingestion_status(ingestion_id: str):
    """
    Check the processing status of an uploaded newspaper.
    
    Returns the current status and extracted content (if complete).
    
    **Statuses**:
    - `queued`: Waiting for processing
    - `processing`: OCR in progress
    - `correcting`: Neural network error correction
    - `completed`: Processing finished
    - `failed`: Processing failed
    """
    # TODO: Query database for ingestion status
    # Placeholder response
    return IngestionStatusResponse(
        status="success",
        data={
            "id": ingestion_id,
            "processing_status": "queued",
            "progress_percent": 0,
            "created_at": datetime.utcnow().isoformat(),
        },
    )



@router.websocket("/ws/notifications")
async def websocket_notifications(ws: WebSocket):
    """WebSocket endpoint for real-time notifications (OCR job events)."""
    await ws_manager.connect(ws)
    try:
        while True:
            # Keep connection open; client may send pings
            data = await ws.receive_text()
            # Echo back minimal acknowledgement
            await ws.send_text(json.dumps({"status": "ok", "received": data}))
    except Exception:
        await ws_manager.disconnect(ws)


@router.get("/history")
async def get_ingestion_history(
    page: int = 1,
    page_size: int = 20,
):
    """
    Get upload history for the authenticated user.
    
    Returns a paginated list of previously uploaded newspapers
    with their processing status and extracted content.
    """
    # TODO: Implement authentication
    # TODO: Query database for user's uploads
    
    return {
        "status": "success",
        "data": [],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_pages": 0,
            "total_items": 0,
            "has_next": False,
            "has_previous": False,
        },
    }


@router.post("/batch")
async def batch_upload(
    images: list[UploadFile] = File(..., description="Multiple newspaper images"),
):
    """
    Upload multiple newspaper images for batch processing.
    
    Accepts up to 10 images per request for efficient bulk processing.
    """
    if len(images) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "TOO_MANY_IMAGES",
                "message": "Maximum 10 images per batch upload",
                "details": {
                    "received": len(images),
                    "max_allowed": 10,
                },
            },
        )
    
    # TODO: Process multiple uploads
    batch_id = str(uuid4())
    
    return {
        "status": "accepted",
        "data": {
            "batch_id": batch_id,
            "total_images": len(images),
            "processing_status": "queued",
        },
        "meta": {
            "timestamp": datetime.utcnow().isoformat(),
        },
    }
