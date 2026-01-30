# Local Development Setup

This file documents how to run the application, worker, and integration tests locally following best practices.

Prerequisites
- Docker & Docker Compose
- Python 3.11 (for running tools locally)
- Optional: Homebrew Postgres for direct DB access

Run services with Docker Compose (recommended)

```bash
# Start Postgres and Redis
docker compose up -d db redis

# Build and start app + worker for development
docker compose -f docker-compose.yml -f docker-compose.override.yml up --build -d
```

Start Celery worker locally (if not using Docker)

```bash
# In project root
pip install -r requirements.txt
celery -A src.worker.celery_app.celery_app worker --loglevel=info
```

Run tests (unit & integration) locally using the built-in test client (no Docker required)

```bash
pip install -r requirements.txt
python -m pytest tests/test_integration_worker.py -q
```

Notes
- Tests use an in-memory SQLite database and monkeypatches for Celery/Redis; they exercise the FastAPI routes without requiring external services.
- For full end-to-end validation, run the CI compose (`docker-compose.ci.yml`) which launches Postgres, Redis, app, and a Celery worker.
