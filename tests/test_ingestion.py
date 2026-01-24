"""Tests for ingestion endpoints."""

import io
from PIL import Image


def test_upload_endpoint_exists(client):
    """Test that upload endpoint is accessible."""
    # Create a test image
    img = Image.new('RGB', (100, 100), color='white')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    response = client.post(
        "/api/v1/ingest/upload",
        files={"image": ("test.jpg", img_bytes, "image/jpeg")},
    )
    
    assert response.status_code in [200, 202]


def test_upload_invalid_file_type(client):
    """Test upload with invalid file type."""
    response = client.post(
        "/api/v1/ingest/upload",
        files={"image": ("test.txt", b"not an image", "text/plain")},
    )
    
    assert response.status_code == 400


def test_status_endpoint(client):
    """Test status check endpoint."""
    response = client.get("/api/v1/ingest/status/test-id-123")
    assert response.status_code == 200


def test_history_endpoint(client):
    """Test history endpoint."""
    response = client.get("/api/v1/ingest/history")
    assert response.status_code == 200
    data = response.json()
    assert "pagination" in data
