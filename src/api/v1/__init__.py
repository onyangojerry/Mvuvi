"""API v1 router."""

from fastapi import APIRouter

from src.api.v1 import ingest, feed, health, ocr, news

router = APIRouter()

# Include sub-routers
router.include_router(health.router, prefix="/health", tags=["Health"])
router.include_router(ocr.router, prefix="/ocr", tags=["OCR"])
router.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])
router.include_router(feed.router, prefix="/feed", tags=["News Feed"])
router.include_router(news.router, prefix="/news", tags=["News"])
