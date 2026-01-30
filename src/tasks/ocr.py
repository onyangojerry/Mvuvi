import time
import json
import os
from pathlib import Path

from src.worker.celery_app import celery_app
from src.config import get_settings
import redis

settings = get_settings()


@celery_app.task(name="src.tasks.ocr.process_ocr")
def process_ocr(file_path: str, ingestion_id: str, job_id: str, language: str = "en"):
    """Simple OCR task placeholder. In production this will call Tesseract/EasyOCR.

    The task publishes a completion event to Redis when done.
    """
    start = time.time()
    # Simulate OCR processing
    text = "[simulated OCR output]"
    time.sleep(1)
    duration_ms = int((time.time() - start) * 1000)

    # Publish result to Redis notifications channel
    try:
        r = redis.Redis.from_url(settings.redis_url, decode_responses=True)
        payload = {
            "event": "ocr_completed",
            "job_id": job_id,
            "ingestion_id": ingestion_id,
            "file_path": file_path,
            "text": text,
            "processing_time_ms": duration_ms,
        }
        r.publish(settings.redis_notifications_channel, json.dumps(payload))
    except Exception:
        # Best-effort publish; do not fail the task for publish errors
        pass

    return {"job_id": job_id, "status": "completed", "processing_time_ms": duration_ms}
