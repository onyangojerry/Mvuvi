"""OCR processing endpoints for text extraction from images."""

import os
import tempfile
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel, Field

from src.services.ocr_service import get_ocr_service

router = APIRouter()


class OCRResult(BaseModel):
    """OCR extraction result."""
    
    text: str = Field(description="Extracted text")
    confidence: float = Field(description="Confidence score (0-1)")
    word_count: int = Field(description="Number of words extracted")
    language: str = Field(description="Language used")
    engine: str = Field(description="OCR engine used")
    processing_time_seconds: float = Field(description="Processing time")


class OCRResponse(BaseModel):
    """Response model for OCR endpoints."""
    
    status: str = Field(default="success")
    data: OCRResult
    meta: dict = Field(description="Request metadata")


class MultiEngineOCRResponse(BaseModel):
    """Response for multi-engine OCR."""
    
    status: str = Field(default="success")
    data: dict = Field(description="Results from multiple engines")
    meta: dict


class EngineInfo(BaseModel):
    """OCR engine information."""
    
    name: str
    available: bool
    description: str
    features: List[str]


@router.get("/engines", summary="List available OCR engines")
async def list_ocr_engines():
    """
    Get list of available OCR engines.
    
    Returns information about installed and available OCR engines:
    - Tesseract: Popular, supports 100+ languages, free
    - EasyOCR: Deep learning-based, high accuracy
    - PaddleOCR: Lightweight, fast, optimized for speed
    """
    ocr_service = get_ocr_service()
    available_engines = ocr_service.available_engines()
    
    engines_info = {
        "tesseract": EngineInfo(
            name="Tesseract",
            available="tesseract" in available_engines,
            description="Most popular open-source OCR engine, supports 100+ languages",
            features=["Multi-language", "Fast", "Widely supported"]
        ),
        "easyocr": EngineInfo(
            name="EasyOCR",
            available="easyocr" in available_engines,
            description="Deep learning-based OCR with high accuracy",
            features=["High accuracy", "80+ languages", "Neural network-based"]
        ),
        "paddleocr": EngineInfo(
            name="PaddleOCR",
            available="paddleocr" in available_engines,
            description="Lightweight OCR optimized for speed and efficiency",
            features=["Lightweight", "Fast inference", "Mobile-friendly"]
        ),
    }
    
    return {
        "status": "success",
        "data": {
            "engines": engines_info,
            "available_engines": available_engines,
            "default_engine": available_engines[0] if available_engines else None,
        },
    }


@router.post("/extract", response_model=OCRResponse, summary="Extract text from image")
async def extract_text_from_image(
    image: UploadFile = File(..., description="Image file (PNG, JPG, PDF)"),
    engine: str = Form(default="auto", description="OCR engine: auto, tesseract, easyocr, paddleocr"),
    language: str = Form(default="en", description="Language code (e.g., 'en', 'es', 'fr')"),
    preprocess: bool = Form(default=True, description="Apply image preprocessing"),
):
    """
    Extract text from an uploaded image using OCR.
    
    This endpoint processes images and extracts text using lightweight,
    open-source OCR engines:
    
    **Supported Engines**:
    - `auto`: Automatically select best available engine
    - `tesseract`: Use Tesseract OCR (most compatible)
    - `easyocr`: Use EasyOCR (highest accuracy)
    - `paddleocr`: Use PaddleOCR (fastest)
    
    **Image Preprocessing** (enabled by default):
    - Grayscale conversion
    - Noise reduction
    - Adaptive thresholding
    - Deskewing
    
    **Supported Languages**: en, es, fr, de, zh, ja, and many more
    (depends on installed OCR engine)
    
    **Example**:
    ```bash
    curl -X POST "http://localhost:8000/api/v1/ocr/extract" \\
      -F "image=@newspaper.jpg" \\
      -F "engine=tesseract" \\
      -F "language=en"
    ```
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "application/pdf"]
    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_IMAGE_FORMAT",
                "message": f"Unsupported file type: {image.content_type}",
                "supported_formats": allowed_types,
            },
        )
    
    # Save uploaded file to temp location
    file_extension = os.path.splitext(image.filename)[1] or ".jpg"
    temp_path = tempfile.mktemp(suffix=file_extension)
    
    try:
        # Save file
        contents = await image.read()
        with open(temp_path, "wb") as f:
            f.write(contents)
        
        # Get OCR service
        ocr_service = get_ocr_service()
        
        # Check if any engine is available
        if not ocr_service.available_engines():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "code": "NO_OCR_ENGINE_AVAILABLE",
                    "message": "No OCR engine is installed",
                    "hint": "Install at least one: pip install pytesseract easyocr paddleocr",
                },
            )
        
        # Extract text
        result = await ocr_service.extract_text(
            image_path=temp_path,
            engine=engine,
            language=language,
            preprocess=preprocess,
        )
        
        return OCRResponse(
            status="success",
            data=OCRResult(**result),
            meta={
                "filename": image.filename,
                "file_size_bytes": len(contents),
                "preprocessing_enabled": preprocess,
            },
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_ENGINE",
                "message": str(e),
            },
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "OCR_PROCESSING_FAILED",
                "message": "Failed to process image",
                "error": str(e),
            },
        )
    
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.post("/extract/compare", response_model=MultiEngineOCRResponse, summary="Compare multiple OCR engines")
async def compare_ocr_engines(
    image: UploadFile = File(..., description="Image file to process"),
):
    """
    Extract text using ALL available OCR engines for comparison.
    
    This endpoint runs the same image through all installed OCR engines
    and returns results from each, allowing you to:
    - Compare accuracy across engines
    - Use ensemble methods (voting, averaging)
    - Validate extraction quality
    
    **Note**: This endpoint is slower as it runs multiple engines.
    Use for validation/testing purposes.
    
    **Example Response**:
    ```json
    {
      "tesseract": {
        "text": "Extracted text...",
        "confidence": 0.92
      },
      "easyocr": {
        "text": "Extracted text...",
        "confidence": 0.95
      }
    }
    ```
    """
    # Save uploaded file
    file_extension = os.path.splitext(image.filename)[1] or ".jpg"
    temp_path = tempfile.mktemp(suffix=file_extension)
    
    try:
        contents = await image.read()
        with open(temp_path, "wb") as f:
            f.write(contents)
        
        # Get OCR service
        ocr_service = get_ocr_service()
        
        if not ocr_service.available_engines():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail={
                    "code": "NO_OCR_ENGINE_AVAILABLE",
                    "message": "No OCR engine is installed",
                },
            )
        
        # Extract with all engines
        results = await ocr_service.extract_with_multiple_engines(temp_path)
        
        return MultiEngineOCRResponse(
            status="success",
            data=results,
            meta={
                "filename": image.filename,
                "engines_used": list(results.keys()),
                "file_size_bytes": len(contents),
            },
        )
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@router.post("/extract/batch", summary="Batch OCR processing")
async def batch_ocr_extract(
    images: List[UploadFile] = File(..., description="Multiple images to process"),
    engine: str = Form(default="auto", description="OCR engine to use"),
    language: str = Form(default="en", description="Language code"),
):
    """
    Process multiple images in batch for OCR text extraction.
    
    Efficiently processes multiple images concurrently.
    Maximum 10 images per batch.
    """
    if len(images) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "TOO_MANY_IMAGES",
                "message": "Maximum 10 images per batch",
                "received": len(images),
            },
        )
    
    ocr_service = get_ocr_service()
    results = []
    
    for image in images:
        file_extension = os.path.splitext(image.filename)[1] or ".jpg"
        temp_path = tempfile.mktemp(suffix=file_extension)
        
        try:
            contents = await image.read()
            with open(temp_path, "wb") as f:
                f.write(contents)
            
            result = await ocr_service.extract_text(
                temp_path,
                engine=engine,
                language=language,
            )
            
            results.append({
                "filename": image.filename,
                "status": "success",
                "result": result,
            })
        
        except Exception as e:
            results.append({
                "filename": image.filename,
                "status": "failed",
                "error": str(e),
            })
        
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    return {
        "status": "success",
        "data": {
            "total_images": len(images),
            "successful": sum(1 for r in results if r["status"] == "success"),
            "failed": sum(1 for r in results if r["status"] == "failed"),
            "results": results,
        },
    }
