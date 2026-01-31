
import time
import json
import os
from pathlib import Path
from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from src.worker.celery_app import celery_app
from src.config import get_settings
from src.services.ocr_service import get_ocr_service
from src.services.nlp_utils import categorize_text, rewrite_text
from src.models import Base, Article, Source
import redis

settings = get_settings()

"""
OCR Celery Task Pipeline:
1. Extract text from image using OCR engine.
2. Categorize the article using NLP keyword/topic matching.
3. Rewrite/summarize the article for clarity.
4. Save the article to the database (with category, summary, and metadata).
5. Broadcast the new article to the newsfeed via Redis pubsub for real-time UI update.
"""



@celery_app.task(name="src.tasks.ocr.process_ocr")
def process_ocr(file_path: str, ingestion_id: str, job_id: str, language: str = "en"):
    """
    Full OCR pipeline:
    1. Extract text from image using Tesseract.
    2. Categorize article using NLP keyword/topic matching.
    3. Rewrite/summarize article for clarity.
    4. Save article to DB (with category, summary, and metadata).
    5. Broadcast new article to Redis for real-time newsfeed.
    """
    start = time.time()
    ocr_service = get_ocr_service()
    # 1. OCR extraction
    result = ocr_service.extract_text(file_path, lang=language, preprocess=True)
    text = result.get("text", "")
    confidence = result.get("confidence", 0.0)
    word_count = result.get("word_count", 0)

    # 2. Categorize
    category = categorize_text(text)

    # 3. Rewrite/summarize
    summary = rewrite_text(text)

    # 4. Save to DB (using SQLAlchemy ORM)
    db_url = settings.database_url
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # Ensure source exists or create a generic one for OCR uploads
        source = session.query(Source).filter_by(name="User Uploads").first()
        if not source:
            source = Source(
                id=str(uuid4()),
                name="User Uploads",
                url="",
                category=category,
                feed_type="ocr",
                is_active=True,
                description="User-uploaded newspaper images",
                language=language,
            )
            session.add(source)
            session.commit()

        article = Article(
            id=str(uuid4()),
            source_id=source.id,
            title=summary[:80] or "Untitled OCR Article",
            content=text,
            summary=summary,
            url=f"ocr-upload://{job_id}",
            author=None,
            published_at=datetime.utcnow(),
            image_url=None,
            is_extracted=True,
            extraction_status="success",
            view_count=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(article)
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

    duration_ms = int((time.time() - start) * 1000)

    # 5. Broadcast to Redis for real-time newsfeed
    try:
        r = redis.Redis.from_url(settings.redis_url, decode_responses=True)
        payload = {
            "event": "new_article",
            "job_id": job_id,
            "ingestion_id": ingestion_id,
            "file_path": file_path,
            "title": article.title,
            "content": article.content,
            "summary": article.summary,
            "category": category,
            "published_at": article.published_at.isoformat(),
            "confidence": confidence,
            "word_count": word_count,
            "processing_time_ms": duration_ms,
        }
        r.publish(settings.redis_notifications_channel, json.dumps(payload))
    except Exception:
        pass

    return {"job_id": job_id, "status": "completed", "processing_time_ms": duration_ms, "category": category}
