"""
Comprehensive test suite for OCR endpoints.

Tests cover:
- All OCR engines (Tesseract, EasyOCR, PaddleOCR)
- Fast transcription endpoint
- Multi-engine comparison
- Batch processing
- Error handling
- Security validation
- Performance benchmarks
"""

import pytest
import io
import time
from PIL import Image, ImageDraw, ImageFont
from fastapi.testclient import TestClient


def create_test_image(text: str = "Test OCR Text", size: tuple = (400, 200)) -> bytes:
    """Create a test image with text."""
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    draw.text((20, 80), text, fill='black')
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes


import pytest_asyncio

class TestOCREngines:
    """Test OCR engine availability and functionality."""

    @pytest.mark.asyncio
    async def test_list_engines(self, client):
        response = await client.get("/api/v1/ocr/engines")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "engines" in data["data"]
        assert "available_engines" in data["data"]
        assert len(data["data"]["available_engines"]) > 0

    @pytest.mark.asyncio
    async def test_tesseract_availability(self, client):
        response = await client.get("/api/v1/ocr/engines")
        data = response.json()
        assert "tesseract" in data["data"]["available_engines"]


class TestOCRExtraction:
    """Test OCR text extraction functionality."""

    @pytest.mark.asyncio
    async def test_extract_basic(self, client):
        img_bytes = create_test_image("Hello World")
        response = await client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")},
            data={"engine": "tesseract", "language": "eng"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "text" in data["data"]
        assert "confidence" in data["data"]
        assert "word_count" in data["data"]

    @pytest.mark.asyncio
    async def test_extract_with_preprocessing(self, client):
        img_bytes = create_test_image("Preprocessed Text")
        response = await client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")},
            data={"engine": "tesseract", "preprocess": "true"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data

    @pytest.mark.asyncio
    async def test_extract_without_preprocessing(self, client):
        img_bytes = create_test_image("Fast Extract")
        response = await client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")},
            data={"engine": "tesseract", "preprocess": "false"}
        )
        if response.status_code != 200:
            print("Error response:", response.text)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_extract_invalid_image_type(self, client):
        response = await client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.txt", b"not an image", "text/plain")}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "code" in data["detail"]

    @pytest.mark.asyncio
    async def test_extract_missing_file(self, client):
        response = await client.post(
            "/api/v1/ocr/extract",
            data={"engine": "tesseract"}
        )
        assert response.status_code == 422  # Unprocessable Entity


class TestFastTranscription:
    """Test fast transcription endpoint."""

    @pytest.mark.asyncio
    async def test_transcribe_fast_basic(self, client):
        img_bytes = create_test_image("Fast Transcribe Test")
        response = await client.post(
            "/api/v1/ocr/transcribe-fast",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")}
        )
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert "confidence" in data
        assert "words" in data
        assert "processing_ms" in data

    @pytest.mark.asyncio
    async def test_transcribe_fast_performance(self, client):
        img_bytes = create_test_image("Performance Test")
        start = time.time()
        response = await client.post(
            "/api/v1/ocr/transcribe-fast",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")}
        )
        elapsed = (time.time() - start) * 1000
        assert response.status_code == 200
        # Should complete within 5 seconds for test image
        assert elapsed < 5000

    @pytest.mark.asyncio
    async def test_transcribe_fast_invalid_format(self, client):
        response = await client.post(
            "/api/v1/ocr/transcribe-fast",
            files={"image": ("test.gif", b"fake", "image/gif")}
        )
        assert response.status_code == 400


class TestMultiEngineComparison:
    """Test multi-engine OCR comparison."""

    @pytest.mark.asyncio
    async def test_compare_engines(self, client):
        img_bytes = create_test_image("Multi Engine Test")
        response = await client.post(
            "/api/v1/ocr/extract/compare",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")}
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], dict)
        # Should have at least tesseract results
        assert len(data["data"]) >= 1


class TestBatchProcessing:
    """Test batch OCR processing."""

    @pytest.mark.asyncio
    async def test_batch_process_multiple_images(self, client):
        images = [
            ("test1.jpg", create_test_image("Image 1"), "image/jpeg"),
            ("test2.jpg", create_test_image("Image 2"), "image/jpeg"),
        ]
        response = await client.post(
            "/api/v1/ocr/extract/batch",
            files=[("images", img) for img in images],
            data={"engine": "tesseract"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "results" in data["data"]

    @pytest.mark.asyncio
    async def test_batch_process_limit(self, client):
        images = [
            (f"test{i}.jpg", create_test_image(f"Image {i}"), "image/jpeg")
            for i in range(11)
        ]
        response = await client.post(
            "/api/v1/ocr/extract/batch",
            files=[("images", img) for img in images]
        )
        assert response.status_code == 400
        data = response.json()
        assert "TOO_MANY_IMAGES" in str(data)


class TestSecurityValidation:
    """Test security-related validations."""

    @pytest.mark.asyncio
    async def test_file_size_validation(self, client):
        img_bytes = create_test_image("Size Test", size=(100, 100))
        response = await client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")}
        )
        # Should accept normal sized images
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_sql_injection_in_language_param(self, client):
        img_bytes = create_test_image("Security Test")
        response = await client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")},
            data={"language": "eng' OR '1'='1"}
        )
        # Should handle safely (might fail validation but shouldn't crash)
        assert response.status_code in [200, 400, 422]

    @pytest.mark.asyncio
    async def test_path_traversal_in_filename(self, client):
        img_bytes = create_test_image("Path Test")
        response = await client.post(
            "/api/v1/ocr/extract",
            files={"image": ("../../etc/passwd", img_bytes, "image/jpeg")}
        )
        # Should handle safely
        assert response.status_code in [200, 400]


class TestErrorHandling:
    """Test comprehensive error handling."""

    @pytest.mark.asyncio
    async def test_invalid_engine_name(self, client):
        img_bytes = create_test_image("Error Test")
        response = await client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")},
            data={"engine": "nonexistent_engine"}
        )
        assert response.status_code in [400, 422]

    @pytest.mark.asyncio
    async def test_corrupted_image(self, client):
        response = await client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", b"corrupted data", "image/jpeg")}
        )
        # Should return error, not crash
        assert response.status_code in [400, 500]

    @pytest.mark.asyncio
    async def test_empty_image(self, client):
        response = await client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", b"", "image/jpeg")}
        )
        assert response.status_code in [400, 422, 500]


class TestPerformanceBenchmarks:
    """Performance benchmark tests."""

    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_ocr_performance_baseline(self, client):
        img_bytes = create_test_image("Performance Benchmark")
        times = []
        for _ in range(5):
            start = time.time()
            response = await client.post(
                "/api/v1/ocr/extract",
                files={"image": ("test.jpg", img_bytes, "image/jpeg")},
                data={"engine": "tesseract", "preprocess": "false"}
            )
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)
            assert response.status_code == 200
        avg_time = sum(times) / len(times)
        print(f"\nAverage OCR time: {avg_time:.2f}ms")
        # Should average under 2 seconds for small test images
        assert avg_time < 2000
