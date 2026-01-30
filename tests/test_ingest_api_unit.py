import pytest
from io import BytesIO

from src.worker.celery_app import celery_app


@pytest.mark.asyncio
async def test_upload_endpoint_monkeypatched(monkeypatch, client):
    # Monkeypatch celery send_task and pubsub.publish_event
    def fake_send_task(name, args=None, kwargs=None, **opts):
        return True

    monkeypatch.setattr(celery_app, "send_task", fake_send_task)

    async def fake_publish(channel, payload):
        return None

    monkeypatch.setattr("src.services.pubsub.publish_event", fake_publish)

    file_bytes = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    files = {"image": ("test.png", BytesIO(file_bytes), "image/png")}

    response = await client.post("/api/v1/ingest/upload", files=files)
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "accepted"
    assert "job_id" in data["data"]["attributes"]
