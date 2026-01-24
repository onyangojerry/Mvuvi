"""Test script for fast transcription endpoint."""

import requests
import time
from pathlib import Path

# API endpoint
BASE_URL = "http://localhost:8000"
FAST_TRANSCRIBE_URL = f"{BASE_URL}/api/v1/ocr/transcribe-fast"
REGULAR_EXTRACT_URL = f"{BASE_URL}/api/v1/ocr/extract"

def test_fast_transcription():
    """Test the fast transcription endpoint."""
    
    # You can create a simple test image or use an existing one
    # For this demo, let's create a simple text image
    print("=" * 60)
    print("FAST TRANSCRIPTION ENDPOINT TEST")
    print("=" * 60)
    
    # Test if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"\n[Done] Server is running: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("\n[Urgent] Server is not running!")
        print("Start with: python -m src.main")
        return
    
    # Check available engines
    print("\n--- Checking OCR Engines ---")
    response = requests.get(f"{BASE_URL}/api/v1/ocr/engines")
    engines_data = response.json()
    print(f"Available engines: {engines_data['data']['available_engines']}")
    
    # Create a simple test image with text
    print("\n--- Creating Test Image ---")
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple image with text
        img = Image.new('RGB', (800, 200), color='white')
        d = ImageDraw.Draw(img)
        
        # Use default font
        text = "Fast OCR Transcription Test - Real-time Processing"
        d.text((50, 80), text, fill='black')
        
        test_image_path = "/tmp/test_ocr_image.png"
        img.save(test_image_path)
        print(f"Test image created: {test_image_path}")
        
    except ImportError:
        print("[Warning] PIL not available, skipping image creation")
        print("You can test with your own image file")
        return
    
    # Test 1: Fast transcription
    print("\n--- Test 1: Fast Transcription (/transcribe-fast) ---")
    start = time.time()
    
    with open(test_image_path, 'rb') as f:
        files = {'image': ('test.png', f, 'image/png')}
        response = requests.post(FAST_TRANSCRIBE_URL, files=files)
    
    end = time.time()
    total_time = int((end - start) * 1000)
    
    if response.status_code == 200:
        result = response.json()
        print(f"[Done] Status: {response.status_code}")
        print(f"Extracted text: {result.get('text', '')[:100]}...")
        print(f"Confidence: {result.get('confidence', 0):.2%}")
        print(f"Word count: {result.get('words', 0)}")
        print(f"Processing time (server): {result.get('processing_ms', 0)}ms")
        print(f"Total time (with network): {total_time}ms")
    else:
        print(f"[Urgent] Request failed: {response.status_code}")
        print(f"Error: {response.json()}")
    
    # Test 2: Regular extraction for comparison
    print("\n--- Test 2: Regular Extraction (/extract) for comparison ---")
    start = time.time()
    
    with open(test_image_path, 'rb') as f:
        files = {'image': ('test.png', f, 'image/png')}
        data = {
            'engine': 'tesseract',
            'language': 'eng',
            'preprocess': 'false'  # Same as fast transcribe
        }
        response = requests.post(REGULAR_EXTRACT_URL, files=files, data=data)
    
    end = time.time()
    total_time = int((end - start) * 1000)
    
    if response.status_code == 200:
        result = response.json()
        print(f"[Done] Status: {response.status_code}")
        print(f"Extracted text: {result['data']['text'][:100]}...")
        print(f"Confidence: {result['data']['confidence']:.2%}")
        print(f"Word count: {result['data']['word_count']}")
        print(f"Processing time: {result['data']['processing_time_seconds']:.3f}s")
        print(f"Total time (with network): {total_time}ms")
    else:
        print(f"[Urgent] Request failed: {response.status_code}")
    
    # Performance comparison
    print("\n--- Performance Summary ---")
    print("The /transcribe-fast endpoint is optimized for:")
    print("- Minimal latency (no preprocessing)")
    print("- Simple response format")
    print("- Real-time applications")
    print("\nUse cases:")
    print("- Live document scanning")
    print("- Mobile apps with instant feedback")
    print("- Quick preview/validation")
    print("- High-throughput batch processing")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    test_fast_transcription()
