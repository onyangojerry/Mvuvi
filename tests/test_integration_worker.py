import pytest
import pytest_asyncio
from httpx import AsyncClient
from io import BytesIO

from src.worker.celery_app import celery_app
from src import main as app_module


@pytest.mark.asyncio
async def test_upload_enqueues_job(monkeypatch, client):
    # Stub out celery send_task to avoid needing a running worker
    def fake_send_task(name, args=None, kwargs=None, **opts):
        return True

    monkeypatch.setattr(celery_app, "send_task", fake_send_task)

    # Stub pubsub publish to avoid Redis dependency
    async def fake_publish(channel, payload):
        return None

    monkeypatch.setattr("src.services.pubsub.publish_event", fake_publish)

    # Create a small in-memory PNG-like payload
    file_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    files = {"image": ("test.png", BytesIO(file_bytes), "image/png")}

    response = await client.post("/api/v1/ingest/upload", files=files)
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "accepted"
    assert "job_id" in data["data"]["attributes"]
