
# OCR-to-NewsFeed Pipeline: Production Implementation (2026-01-31)

## Overview
This document describes the full, productionized pipeline for user-uploaded newspaper images, including OCR extraction, NLP-based categorization and rewriting, database storage, and real-time news feed display. It also documents the real-time WebSocket/Redis integration and Celery worker registration fixes.

---

## Pipeline Steps

### 1. Upload (Frontend)
- **OCRPanel**: User uploads an image and clicks "Upload to News Feed".
- **Endpoint**: POST `/api/v1/ingest/upload` (FastAPI)

### 2. Ingestion (Backend)
- **Validation**: File type and size checked.
- **Storage**: Image saved to persistent storage.
- **Job Creation**: An `OCRJob` is created in the DB.
- **Task Enqueue**: Celery task `src.tasks.ocr.process_ocr` is enqueued with file path and job info.

### 3. OCR Processing (Celery Worker)
- **Task Registration**: Celery worker imports `src.tasks.ocr` to register the task.
- **Extraction**: Tesseract OCR extracts text from the image.
- **NLP Categorization**: `categorize_text` assigns a category (technology, world, business, science, general).
- **NLP Rewriting**: `rewrite_text` generates a summary/rewritten version.
- **DB Storage**: Article is saved to the `Article` table, linked to a `Source` ("User Uploads").
- **Real-Time Event**: Publishes a `new_article` event to Redis notifications channel.

### 4. Real-Time News Feed (Backend & Frontend)
- **WebSocket Endpoint**: `/api/v1/feed/stream` (FastAPI)
- **On Connect**: Streams all articles from DB to client.
- **Redis Subscription**: Subscribes to Redis notifications; on `new_article`, broadcasts to all connected clients.
- **Frontend**: `useNewsStream` hook listens for `new_article` and updates the news feed in real time.

### 5. Feed API (Initial Load)
- **Endpoint**: `/api/v1/feed`
- **Fix**: Now queries the DB for all articles, paginates, and returns them to the frontend.

---

## Key Code/Config Changes
- **Celery Worker Registration**: `src/worker/celery_app.py` now imports `src.tasks.ocr` to register the OCR task.
- **Feed Endpoint**: `/api/v1/feed` now uses `len(...scalars().all())` for total count (fixes AttributeError).
- **WebSocket/Redis Bridge**: `/api/v1/feed/stream` subscribes to Redis and broadcasts new articles in real time.
- **Frontend WebSocket Handler**: `useNewsStream.ts` now uses `message.article` for real-time updates.
- **Error Logging**: Ingestion endpoint logs and returns detailed tracebacks for easier debugging.

---

## Testing & Deployment
- **Docker**: Rebuild and restart all containers after code changes.
- **Celery**: Ensure worker is started with the correct app and imports.
- **Frontend**: Run `npm run dev` for local development.

---

## References
- `src/api/v1/ingest.py`: Upload endpoint, error logging
- `src/tasks/ocr.py`: Celery OCR pipeline, NLP, DB, Redis
- `src/worker/celery_app.py`: Celery app, task registration
- `src/api/v1/feed.py`: Feed API, WebSocket, Redis bridge
- `src/services/nlp_utils.py`: Categorization and rewriting
- `mvuvi-ui/src/hooks/useNewsStream.ts`: Real-time frontend updates
- `mvuvi-ui/src/panels/NewsFeedPanel.tsx`: News feed UI

---

## Changelog (2026-01-31)
- Fix: Celery worker task registration for OCR jobs
- Fix: Feed API total count bug
- Feature: Real-time Redis-to-WebSocket news updates
- Fix: Frontend WebSocket handler for new articles
- Docs: Full pipeline and troubleshooting guide
