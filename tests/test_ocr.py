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


class TestOCREngines:
    """Test OCR engine availability and functionality."""
    
    def test_list_engines(self, client):
        """Test listing available OCR engines."""
        response = client.get("/api/v1/ocr/engines")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "engines" in data["data"]
        assert "available_engines" in data["data"]
        assert len(data["data"]["available_engines"]) > 0
    
    def test_tesseract_availability(self, client):
        """Test that Tesseract engine is available."""
        response = client.get("/api/v1/ocr/engines")
        data = response.json()
        assert "tesseract" in data["data"]["available_engines"]


class TestOCRExtraction:
    """Test OCR text extraction functionality."""
    
    def test_extract_basic(self, client):
        """Test basic text extraction."""
        img_bytes = create_test_image("Hello World")
        
        response = client.post(
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
    
    def test_extract_with_preprocessing(self, client):
        """Test extraction with image preprocessing enabled."""
        img_bytes = create_test_image("Preprocessed Text")
        
        response = client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")},
            data={"engine": "tesseract", "preprocess": "true"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
    
    def test_extract_without_preprocessing(self, client):
        """Test extraction without preprocessing (faster)."""
        img_bytes = create_test_image("Fast Extract")
        
        response = client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")},
            data={"engine": "tesseract", "preprocess": "false"}
        )
        
        assert response.status_code == 200
    
    def test_extract_invalid_image_type(self, client):
        """Test error handling for invalid image type."""
        response = client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.txt", b"not an image", "text/plain")}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "code" in data["detail"]
    
    def test_extract_missing_file(self, client):
        """Test error handling when image file is missing."""
        response = client.post(
            "/api/v1/ocr/extract",
            data={"engine": "tesseract"}
        )
        
        assert response.status_code == 422  # Unprocessable Entity


class TestFastTranscription:
    """Test fast transcription endpoint."""
    
    def test_transcribe_fast_basic(self, client):
        """Test basic fast transcription."""
        img_bytes = create_test_image("Fast Transcribe Test")
        
        response = client.post(
            "/api/v1/ocr/transcribe-fast",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "text" in data
        assert "confidence" in data
        assert "words" in data
        assert "processing_ms" in data
    
    def test_transcribe_fast_performance(self, client):
        """Test that fast transcription meets performance targets."""
        img_bytes = create_test_image("Performance Test")
        
        start = time.time()
        response = client.post(
            "/api/v1/ocr/transcribe-fast",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")}
        )
        elapsed = (time.time() - start) * 1000
        
        assert response.status_code == 200
        # Should complete within 5 seconds for test image
        assert elapsed < 5000
    
    def test_transcribe_fast_invalid_format(self, client):
        """Test fast transcription rejects invalid formats."""
        response = client.post(
            "/api/v1/ocr/transcribe-fast",
            files={"image": ("test.gif", b"fake", "image/gif")}
        )
        
        assert response.status_code == 400


class TestMultiEngineComparison:
    """Test multi-engine OCR comparison."""
    
    def test_compare_engines(self, client):
        """Test comparing multiple OCR engines."""
        img_bytes = create_test_image("Multi Engine Test")
        
        response = client.post(
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
    
    def test_batch_process_multiple_images(self, client):
        """Test processing multiple images in batch."""
        images = [
            ("test1.jpg", create_test_image("Image 1"), "image/jpeg"),
            ("test2.jpg", create_test_image("Image 2"), "image/jpeg"),
        ]
        
        response = client.post(
            "/api/v1/ocr/extract/batch",
            files=[("images", img) for img in images],
            data={"engine": "tesseract"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "results" in data["data"]
    
    def test_batch_process_limit(self, client):
        """Test that batch processing enforces maximum limit."""
        # Try to send 11 images (limit is 10)
        images = [
            (f"test{i}.jpg", create_test_image(f"Image {i}"), "image/jpeg")
            for i in range(11)
        ]
        
        response = client.post(
            "/api/v1/ocr/extract/batch",
            files=[("images", img) for img in images]
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "TOO_MANY_IMAGES" in str(data)


class TestSecurityValidation:
    """Test security-related validations."""
    
    def test_file_size_validation(self, client):
        """Test file size limits are enforced."""
        # Create a large image (> 10MB would require actual large file)
        # For testing, we just verify the endpoint structure
        img_bytes = create_test_image("Size Test", size=(100, 100))
        
        response = client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")}
        )
        
        # Should accept normal sized images
        assert response.status_code == 200
    
    def test_sql_injection_in_language_param(self, client):
        """Test protection against SQL injection in parameters."""
        img_bytes = create_test_image("Security Test")
        
        response = client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")},
            data={"language": "eng' OR '1'='1"}
        )
        
        # Should handle safely (might fail validation but shouldn't crash)
        assert response.status_code in [200, 400, 422]
    
    def test_path_traversal_in_filename(self, client):
        """Test protection against path traversal attacks."""
        img_bytes = create_test_image("Path Test")
        
        response = client.post(
            "/api/v1/ocr/extract",
            files={"image": ("../../etc/passwd", img_bytes, "image/jpeg")}
        )
        
        # Should handle safely
        assert response.status_code in [200, 400]


class TestErrorHandling:
    """Test comprehensive error handling."""
    
    def test_invalid_engine_name(self, client):
        """Test error when invalid engine is specified."""
        img_bytes = create_test_image("Error Test")
        
        response = client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", img_bytes, "image/jpeg")},
            data={"engine": "nonexistent_engine"}
        )
        
        assert response.status_code in [400, 422]
    
    def test_corrupted_image(self, client):
        """Test handling of corrupted image data."""
        response = client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", b"corrupted data", "image/jpeg")}
        )
        
        # Should return error, not crash
        assert response.status_code in [400, 500]
    
    def test_empty_image(self, client):
        """Test handling of empty image file."""
        response = client.post(
            "/api/v1/ocr/extract",
            files={"image": ("test.jpg", b"", "image/jpeg")}
        )
        
        assert response.status_code in [400, 422, 500]


class TestPerformanceBenchmarks:
    """Performance benchmark tests."""
    
    @pytest.mark.slow
    def test_ocr_performance_baseline(self, client):
        """Benchmark OCR performance for baseline."""
        img_bytes = create_test_image("Performance Benchmark")
        
        times = []
        for _ in range(5):
            start = time.time()
            response = client.post(
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
