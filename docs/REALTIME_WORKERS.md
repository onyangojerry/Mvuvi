# Real-time notifications and background workers

This document describes the Redis + Celery + WebSocket architecture implemented for processing OCR jobs and broadcasting events.

Overview
- Worker: Celery with Redis broker/ backend (`celery[redis]`) runs tasks in `src.tasks.ocr.process_ocr`.
- Pub/Sub: Redis used for lightweight notifications on `vuva:notifications` channel.
- WebSockets: FastAPI WebSocket manager subscribes to Redis and broadcasts to connected clients.

Developer setup
1. Ensure Redis is running locally (docker-compose includes `redis` service).
2. Install dependencies: `pip install -r requirements.txt` (includes `celery[redis]`).
3. Start a Celery worker in the project root:

```bash
celery -A src.worker.celery_app.celery_app worker --loglevel=info
```

4. Start the app (local dev):

```bash
uvicorn src.main:app --reload
```

Flow
1. Client uploads an image via `/api/v1/upload`.
2. The API saves the file to `./uploads`, creates an `OCRJob` row, publishes `ocr_job_created` to Redis and enqueues `src.tasks.ocr.process_ocr`.
3. The Celery worker processes the image, then publishes `ocr_completed` to Redis with results.
4. The FastAPI app has a background Redis subscriber that forwards messages to connected WebSocket clients.

Security & Operational notes
- Use Redis TLS/auth in production and restrict access.
- Run Celery workers with supervisor / systemd or Kubernetes deployments.
- Configure proper concurrency and CPU/memory limits for OCR workers (OCR is CPU-bound).
