"""Tests for ingestion endpoints."""

import io
from PIL import Image


import pytest

@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires explicit image input for upload.")
async def test_upload_endpoint_exists(client):
    pass


@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires explicit image input for upload.")
async def test_upload_invalid_file_type(client):
    pass


@pytest.mark.asyncio
async def test_status_endpoint(client):
    """Test status check endpoint."""
    response = await client.get("/api/v1/ingest/status/test-id-123")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_history_endpoint(client):
    """Test history endpoint."""
    response = await client.get("/api/v1/ingest/history")
    assert response.status_code == 200
    data = response.json()
    assert "pagination" in data
