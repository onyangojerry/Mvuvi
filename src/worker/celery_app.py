from celery import Celery
from src.config import get_settings

settings = get_settings()

celery_app = Celery(
    "mvuvi",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)


# Ensure all task modules are imported so Celery can discover them
import src.tasks.ocr

__all__ = ["celery_app"]
