# Fast Transcription Endpoint Guide

## Overview

The `/api/v1/ocr/transcribe-fast` endpoint provides immediate, low-latency text extraction from images, optimized for real-time applications.

## Key Features

- **Ultra-fast processing**: ~100-300ms for typical images
- **No preprocessing**: Skips image enhancement for speed
- **Minimal response**: Only essential data returned
- **Tesseract-powered**: Uses the fastest OCR engine
- **Simple API**: Single file upload, instant results

## When to Use

### Use Fast Transcription For:
- Live document scanning applications
- Mobile apps requiring instant feedback
- Quick preview/validation workflows
- High-throughput batch processing
- Real-time transcription displays
- User-facing features where speed matters

### Use Regular `/extract` For:
- High-accuracy requirements
- Poor quality images needing preprocessing
- When you need detailed metadata
- Multiple engine comparison
- Archival/permanent records

## Performance Comparison

| Feature | `/transcribe-fast` | `/extract` (no preprocess) |
|---------|-------------------|----------------------------|
| Processing Time | ~100-300ms | ~150-350ms |
| Response Size | Minimal (~200 bytes) | Full (~500 bytes) |
| Metadata | Basic (text, confidence, words) | Comprehensive (engine, language, timing) |
| Best For | Real-time UX | Production processing |

## API Reference

### Endpoint
```
POST /api/v1/ocr/transcribe-fast
```

### Request

**Content-Type**: `multipart/form-data`

**Parameters**:
- `image` (required): Image file (PNG, JPG)
  - Max size: 10MB (configurable)
  - Supported formats: PNG, JPEG

### Response

**Success (200)**:
```json
{
  "text": "Extracted text content here...",
  "confidence": 0.87,
  "words": 245,
  "processing_ms": 156
}
```

**Fields**:
- `text` (string): Extracted text from the image
- `confidence` (float): OCR confidence score (0.0-1.0)
- `words` (int): Number of words extracted
- `processing_ms` (int): Server processing time in milliseconds

**Error (400 - Invalid Image)**:
```json
{
  "detail": {
    "code": "INVALID_IMAGE_FORMAT",
    "message": "Unsupported file type: image/gif",
    "supported_formats": ["image/jpeg", "image/png", "image/jpg"]
  }
}
```

**Error (503 - Tesseract Not Available)**:
```json
{
  "detail": {
    "code": "TESSERACT_NOT_AVAILABLE",
    "message": "Fast transcription requires Tesseract OCR",
    "hint": "Install with: brew install tesseract"
  }
}
```

## Usage Examples

### Python (requests)

```python
import requests

# Simple transcription
with open('document.jpg', 'rb') as f:
    files = {'image': f}
    response = requests.post(
        'http://localhost:8000/api/v1/ocr/transcribe-fast',
        files=files
    )

result = response.json()
print(f"Text: {result['text']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Processing time: {result['processing_ms']}ms")
```

### Python (async with aiohttp)

```python
import aiohttp

async def transcribe_image(image_path):
    async with aiohttp.ClientSession() as session:
        with open(image_path, 'rb') as f:
            data = aiohttp.FormData()
            data.add_field('image', f, filename='image.jpg')
            
            async with session.post(
                'http://localhost:8000/api/v1/ocr/transcribe-fast',
                data=data
            ) as response:
                return await response.json()

# Usage
result = await transcribe_image('scan.jpg')
```

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/ocr/transcribe-fast" \
  -F "image=@newspaper.jpg"
```

### JavaScript (Fetch API)

```javascript
async function transcribeImage(file) {
  const formData = new FormData();
  formData.append('image', file);
  
  const response = await fetch(
    'http://localhost:8000/api/v1/ocr/transcribe-fast',
    {
      method: 'POST',
      body: formData
    }
  );
  
  return await response.json();
}

// Usage with file input
const fileInput = document.getElementById('imageInput');
const file = fileInput.files[0];
const result = await transcribeImage(file);
console.log(result.text);
```

### JavaScript (Node.js with axios)

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

async function transcribe(imagePath) {
  const form = new FormData();
  form.append('image', fs.createReadStream(imagePath));
  
  const response = await axios.post(
    'http://localhost:8000/api/v1/ocr/transcribe-fast',
    form,
    { headers: form.getHeaders() }
  );
  
  return response.data;
}

// Usage
transcribe('./document.jpg').then(result => {
  console.log(`Text: ${result.text}`);
  console.log(`Speed: ${result.processing_ms}ms`);
});
```

## Real-World Examples

### 1. Live Scanner App

```python
"""Real-time document scanner with instant preview."""
import cv2
import requests
from PIL import Image
import io

def scan_and_transcribe():
    """Capture from camera and transcribe in real-time."""
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Display frame
        cv2.imshow('Scanner', frame)
        
        # Press 's' to scan
        if cv2.waitKey(1) & 0xFF == ord('s'):
            # Convert to PIL Image
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            
            # Save to bytes
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format='JPEG')
            img_byte_arr.seek(0)
            
            # Transcribe
            files = {'image': ('scan.jpg', img_byte_arr, 'image/jpeg')}
            response = requests.post(
                'http://localhost:8000/api/v1/ocr/transcribe-fast',
                files=files
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\nExtracted text ({result['processing_ms']}ms):")
                print(result['text'])
                print(f"Confidence: {result['confidence']:.2%}")
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
```

### 2. Batch Processing with Progress

```python
"""Process multiple images with progress tracking."""
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def transcribe_single(image_path):
    """Transcribe a single image."""
    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(
            'http://localhost:8000/api/v1/ocr/transcribe-fast',
            files=files
        )
        return {
            'path': image_path,
            'result': response.json() if response.ok else None,
            'status': response.status_code
        }

def batch_transcribe(image_folder, max_workers=4):
    """Transcribe all images in a folder."""
    image_files = list(Path(image_folder).glob('*.jpg'))
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(tqdm(
            executor.map(transcribe_single, image_files),
            total=len(image_files),
            desc="Transcribing"
        ))
    
    return results

# Usage
results = batch_transcribe('./scans', max_workers=4)
successful = [r for r in results if r['result']]
print(f"Processed {len(successful)}/{len(results)} images")
```

### 3. React Web App Component

```jsx
import React, { useState } from 'react';

function FastTranscriber() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    
    setLoading(true);
    const formData = new FormData();
    formData.append('image', file);
    
    try {
      const response = await fetch(
        'http://localhost:8000/api/v1/ocr/transcribe-fast',
        {
          method: 'POST',
          body: formData
        }
      );
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Transcription failed:', error);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="transcriber">
      <input 
        type="file" 
        accept="image/jpeg,image/png"
        onChange={handleImageUpload}
      />
      
      {loading && <p>Transcribing...</p>}
      
      {result && (
        <div className="result">
          <h3>Extracted Text ({result.processing_ms}ms)</h3>
          <p>{result.text}</p>
          <small>
            Confidence: {(result.confidence * 100).toFixed(1)}% | 
            Words: {result.words}
          </small>
        </div>
      )}
    </div>
  );
}
```

## Optimization Tips

### Client-Side
1. **Compress images before upload**: Reduce to 1-2MB for faster transmission
2. **Use appropriate resolution**: 300 DPI is ideal, higher is unnecessary
3. **Implement retry logic**: Handle transient failures
4. **Show progress indicators**: Improve perceived performance

```python
# Example: Image compression before upload
from PIL import Image

def compress_image(image_path, max_size_mb=2):
    """Compress image to target size."""
    img = Image.open(image_path)
    
    # Resize if too large
    max_dimension = 3000
    if max(img.size) > max_dimension:
        ratio = max_dimension / max(img.size)
        new_size = tuple(int(dim * ratio) for dim in img.size)
        img = img.resize(new_size, Image.LANCZOS)
    
    # Save with compression
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=85, optimize=True)
    return output.getvalue()
```

### Server-Side
1. **Increase worker processes**: Use multiple Uvicorn workers
2. **Enable HTTP/2**: Faster for concurrent requests
3. **Configure caching**: Cache results for identical images
4. **Monitor performance**: Track processing times

```bash
# Production deployment with multiple workers
uvicorn src.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info
```

## Troubleshooting

### Slow Performance
- **Check image size**: Large images (>5MB) take longer
- **Monitor CPU**: OCR is CPU-intensive
- **Review logs**: Check for preprocessing issues

### Low Accuracy
- **Image quality**: Blurry or low-contrast images reduce accuracy
- **Use `/extract` with preprocessing**: For difficult images
- **Check language**: Ensure text language matches

### Rate Limiting
- **Implement client-side throttling**: Limit concurrent requests
- **Use batch endpoints**: For multiple images
- **Consider queuing**: For high-volume processing

## See Also

- [OCR Service Documentation](api%20architecture.md)
- [Regular `/extract` endpoint](../src/api/v1/ocr.py)
- [Performance Tuning Guide](../README.md#performance)
