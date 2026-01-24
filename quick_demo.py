"""
Quick demo: Upload and transcribe an image in real-time
Usage: python quick_demo.py <image_path>
"""

import sys
import requests
import time

def quick_transcribe(image_path):
    """Upload an image and get instant transcription."""
    
    url = "http://localhost:8000/api/v1/ocr/transcribe-fast"
    
    print(f"\nTranscribing: {image_path}")
    print("-" * 50)
    
    start = time.time()
    
    try:
        with open(image_path, 'rb') as f:
            files = {'image': ('image.jpg', f, 'image/jpeg')}
            response = requests.post(url, files=files)
        
        elapsed = int((time.time() - start) * 1000)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"[Done] Transcription complete!")
            print(f"\nText ({result['words']} words):")
            print(result['text'])
            print(f"\nConfidence: {result['confidence']:.2%}")
            print(f"Server processing: {result['processing_ms']}ms")
            print(f"Total time (with upload): {elapsed}ms")
        else:
            print(f"[Error] Status: {response.status_code}")
            print(response.json())
    
    except FileNotFoundError:
        print(f"[Error] File not found: {image_path}")
    except requests.exceptions.ConnectionError:
        print("[Error] Cannot connect to server")
        print("Make sure the API is running: python -m src.main")
    except Exception as e:
        print(f"[Error] {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python quick_demo.py <image_path>")
        print("\nExample:")
        print("  python quick_demo.py /tmp/test_ocr_image.png")
        sys.exit(1)
    
    quick_transcribe(sys.argv[1])
