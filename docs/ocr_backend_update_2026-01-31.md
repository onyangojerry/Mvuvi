# OCR Backend Update (2026-01-31)

## Summary
- Migrated backend OCR service to use only Tesseract for lightweight, reliable image-to-text extraction.
- Removed EasyOCR and PaddleOCR dependencies from requirements and service code.
- Ensured Tesseract system binary and language data are installed in Docker image.
- Added robust engine detection and logging to backend for easier debugging.
- Updated frontend and backend integration for seamless OCR processing.

## Key Changes

### 1. requirements.txt
- Removed: easyocr, paddleocr, paddlepaddle
- Kept: pytesseract, Pillow, opencv-python-headless, pdf2image

### 2. Dockerfile
- Ensured installation of tesseract-ocr and tesseract-ocr-eng system packages.

### 3. src/services/ocr_service.py
- Only Tesseract is initialized and used.
- Added startup log: prints Tesseract version and available engines.
- Improved detection logic for Tesseract availability.

### 4. src/api/v1/ocr.py
- Improved error logging and tracebacks for easier debugging.

### 5. mvuvi-ui/vite.config.ts
- Added dev server proxy for /api to backend, avoiding CORS issues.
- Documented proxy setup in code comments.

## Usage
- To rebuild and run: `docker compose build --no-cache && docker compose up`
- OCR endpoint now uses Tesseract only, for maximum reliability and minimal dependencies.

## Troubleshooting
- If OCR fails, check backend logs for [OCR INIT] and [OCR ERROR] messages.
- Ensure Tesseract is installed and detected in the container.

---
