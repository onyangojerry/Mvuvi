# Vuva API Documentation

**Version**: 1.2.1  
**Last Updated**: January 24, 2026  
**Base URL**: `http://localhost:8000`  
**API Prefix**: `/api/v1`

## Overview

Vuva provides a RESTful API for newspaper ingestion, OCR processing, news aggregation, and personalized feed delivery with enterprise-grade security.

## Authentication

### Methods

1. **JWT Tokens** (Recommended for web/mobile apps)
   - Access token (15-minute expiry)
   - Refresh token (7-day expiry)

2. **API Keys** (For programmatic access)
   - Long-lived tokens
   - Can be revoked anytime

### Getting Started

#### 1. Register a User
```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}

# Response
{
  "id": "uuid",
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2026-01-24T12:00:00Z"
}
```

#### 2. Login
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### 3. Use Access Token
```bash
GET /api/v1/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

# Response
{
  "id": "uuid",
  "email": "user@example.com",
  "is_active": true
}
```

## API Endpoints

### Health & Status

#### GET /
Root endpoint with API information

**Response**:
```json
{
  "message": "Vuva Newspaper Ingestion API",
  "version": "1.2.1",
  "docs": "/docs",
  "status": "operational"
}
```

#### GET /health
Basic health check

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-24T12:00:00Z"
}
```

#### GET /api/v1/health
Detailed health check with component status

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-24T12:00:00Z",
  "components": {
    "database": "healthy",
    "cache": "healthy",
    "ocr": "healthy"
  },
  "version": "1.2.1"
}
```

---

### Authentication Endpoints

All endpoints under `/api/v1/auth`

#### POST /api/v1/auth/register
Register a new user

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Password Requirements**:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

**Response**: `201 Created`
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2026-01-24T12:00:00Z"
}
```

#### POST /api/v1/auth/login
Login and get JWT tokens

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### POST /api/v1/auth/refresh
Refresh access token using refresh token

**Request**:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### GET /api/v1/auth/me
Get current authenticated user

**Headers**: `Authorization: Bearer <access_token>`

**Response**: `200 OK`
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2026-01-24T12:00:00Z"
}
```

#### POST /api/v1/auth/change-password
Change user password

**Headers**: `Authorization: Bearer <access_token>`

**Request**:
```json
{
  "current_password": "OldPass123",
  "new_password": "NewSecurePass456"
}
```

**Response**: `200 OK`
```json
{
  "message": "Password changed successfully"
}
```

#### POST /api/v1/auth/api-keys
Generate a new API key

**Headers**: `Authorization: Bearer <access_token>`

**Request**:
```json
{
  "name": "My Integration Key"
}
```

**Response**: `201 Created`
```json
{
  "id": "uuid",
  "key": "vva_live_1234567890abcdef",
  "name": "My Integration Key",
  "created_at": "2026-01-24T12:00:00Z"
}
```

⚠️ **Important**: Save the `key` value - it will not be shown again!

#### GET /api/v1/auth/api-keys
List user's API keys

**Headers**: `Authorization: Bearer <access_token>`

**Response**: `200 OK`
```json
[
  {
    "id": "uuid",
    "name": "My Integration Key",
    "created_at": "2026-01-24T12:00:00Z",
    "last_used": "2026-01-24T13:30:00Z"
  }
]
```

#### DELETE /api/v1/auth/api-keys/{key_id}
Revoke an API key

**Headers**: `Authorization: Bearer <access_token>`

**Response**: `204 No Content`

---

### OCR Endpoints

All endpoints under `/api/v1/ocr`

#### GET /api/v1/ocr/engines
List available OCR engines

**Response**: `200 OK`
```json
{
  "engines": [
    {
      "name": "tesseract",
      "available": true,
      "version": "5.0.0"
    },
    {
      "name": "easyocr",
      "available": true,
      "languages": ["en", "sw"]
    },
    {
      "name": "paddleocr",
      "available": true,
      "languages": ["en", "sw"]
    }
  ]
}
```

#### POST /api/v1/ocr/extract
Extract text from an image using a specific engine

**Headers**: `Authorization: Bearer <access_token>`

**Request**: `multipart/form-data`
- `file`: Image file (JPEG, PNG, TIFF)
- `engine`: OCR engine name (tesseract, easyocr, paddleocr)
- `language`: Language code (default: en)
- `preprocess`: Enable preprocessing (default: true)

**Example**:
```bash
curl -X POST http://localhost:8000/api/v1/ocr/extract \
  -H "Authorization: Bearer <token>" \
  -F "file=@newspaper.jpg" \
  -F "engine=tesseract" \
  -F "language=en" \
  -F "preprocess=true"
```

**Response**: `200 OK`
```json
{
  "text": "Extracted text from the image...",
  "engine": "tesseract",
  "language": "en",
  "confidence": 0.95,
  "processing_time": 1.23
}
```

#### POST /api/v1/ocr/transcribe/fast
Fast transcription optimized for speed

**Headers**: `Authorization: Bearer <access_token>`

**Request**: `multipart/form-data`
- `file`: Image file
- `language`: Language code (default: en)

**Response**: `200 OK`
```json
{
  "text": "Extracted text...",
  "engine": "tesseract",
  "processing_time": 0.45
}
```

#### POST /api/v1/ocr/compare
Compare results from all OCR engines

**Headers**: `Authorization: Bearer <access_token>`

**Request**: `multipart/form-data`
- `file`: Image file
- `language`: Language code (default: en)

**Response**: `200 OK`
```json
{
  "results": [
    {
      "engine": "tesseract",
      "text": "Text from Tesseract...",
      "confidence": 0.95,
      "processing_time": 1.2
    },
    {
      "engine": "easyocr",
      "text": "Text from EasyOCR...",
      "confidence": 0.92,
      "processing_time": 2.1
    },
    {
      "engine": "paddleocr",
      "text": "Text from PaddleOCR...",
      "confidence": 0.94,
      "processing_time": 1.8
    }
  ]
}
```

#### POST /api/v1/ocr/batch
Process multiple images in batch

**Headers**: `Authorization: Bearer <access_token>`

**Request**: `multipart/form-data`
- `files`: Multiple image files
- `engine`: OCR engine (default: tesseract)
- `language`: Language code (default: en)

**Response**: `200 OK`
```json
{
  "results": [
    {
      "filename": "page1.jpg",
      "text": "Extracted text...",
      "status": "success"
    },
    {
      "filename": "page2.jpg",
      "text": "Extracted text...",
      "status": "success"
    }
  ],
  "total": 2,
  "successful": 2,
  "failed": 0
}
```

---

### News & Feed Endpoints

All endpoints under `/api/v1/feed` and `/api/v1/news`

#### GET /api/v1/feed
Get personalized news feed

**Headers**: `Authorization: Bearer <access_token>`

**Query Parameters**:
- `category`: Filter by category (optional)
- `language`: Filter by language (optional)
- `limit`: Number of items (default: 20)
- `offset`: Pagination offset (default: 0)

**Response**: `200 OK`
```json
{
  "items": [
    {
      "id": "uuid",
      "title": "News Article Title",
      "summary": "Brief summary...",
      "content": "Full content...",
      "source": "Daily News",
      "category": "technology",
      "published_at": "2026-01-24T10:00:00Z",
      "url": "https://source.com/article"
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

#### GET /api/v1/feed/{article_id}
Get a specific article

**Headers**: `Authorization: Bearer <access_token>`

**Response**: `200 OK`
```json
{
  "id": "uuid",
  "title": "Article Title",
  "content": "Full article content...",
  "source": "Daily News",
  "author": "John Doe",
  "published_at": "2026-01-24T10:00:00Z",
  "url": "https://source.com/article"
}
```

#### GET /api/v1/news/sources
Get list of available news sources

**Response**: `200 OK`
```json
{
  "sources": [
    {
      "id": "bbc-news",
      "name": "BBC News",
      "category": "general",
      "language": "en",
      "country": "gb"
    },
    {
      "id": "techcrunch",
      "name": "TechCrunch",
      "category": "technology",
      "language": "en",
      "country": "us"
    }
  ]
}
```

#### POST /api/v1/feed/preferences
Update user feed preferences

**Headers**: `Authorization: Bearer <access_token>`

**Request**:
```json
{
  "categories": ["technology", "business"],
  "languages": ["en", "sw"],
  "sources": ["bbc-news", "techcrunch"]
}
```

**Response**: `200 OK`
```json
{
  "message": "Preferences updated successfully"
}
```

---

### Document Ingestion Endpoints

All endpoints under `/api/v1/ingest`

#### POST /api/v1/ingest/upload
Upload a document for processing

**Headers**: `Authorization: Bearer <access_token>`

**Request**: `multipart/form-data`
- `file`: Document file (PDF, JPEG, PNG, TIFF)
- `language`: Language code (default: en)
- `priority`: Processing priority (low, normal, high)

**Response**: `202 Accepted`
```json
{
  "job_id": "uuid",
  "status": "queued",
  "message": "Document uploaded and queued for processing"
}
```

#### GET /api/v1/ingest/status/{job_id}
Get processing status of an uploaded document

**Headers**: `Authorization: Bearer <access_token>`

**Response**: `200 OK`
```json
{
  "job_id": "uuid",
  "status": "processing",
  "progress": 45,
  "created_at": "2026-01-24T12:00:00Z",
  "updated_at": "2026-01-24T12:01:00Z"
}
```

**Status Values**:
- `queued`: Waiting to be processed
- `processing`: Currently being processed
- `completed`: Processing finished
- `failed`: Processing failed

#### GET /api/v1/ingest/history
Get user's document processing history

**Headers**: `Authorization: Bearer <access_token>`

**Query Parameters**:
- `limit`: Number of items (default: 20)
- `offset`: Pagination offset (default: 0)

**Response**: `200 OK`
```json
{
  "items": [
    {
      "job_id": "uuid",
      "filename": "document.pdf",
      "status": "completed",
      "created_at": "2026-01-24T12:00:00Z",
      "completed_at": "2026-01-24T12:05:00Z"
    }
  ],
  "total": 50,
  "limit": 20,
  "offset": 0
}
```

---

## Error Responses

All errors follow a consistent format:

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "detail": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "Invalid email format",
      "type": "value_error.email"
    }
  ]
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded. Try again in 60 seconds."
}
```

### 500 Internal Server Error
```json
{
  "detail": "An unexpected error occurred"
}
```

---

## Rate Limits

Rate limits are applied per user/API key:

| Tier | Limit | Window |
|------|-------|--------|
| Free | 100 requests | 1 hour |
| Basic | 1,000 requests | 1 hour |
| Premium | 10,000 requests | 1 hour |

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1706097600
```

---

## Security Features

### Input Validation
- All inputs are sanitized for XSS attacks
- SQL injection prevention (parameterized queries)
- Command injection protection
- Unicode normalization to prevent bypass attacks

### File Upload Security
- Type validation (whitelist-based)
- Size limits (10MB default)
- Double extension detection (.pdf.exe blocked)
- Path traversal prevention

### URL Safety
- Protocol whitelist (http/https only)
- Dangerous protocols blocked (javascript:, data:, file:)
- Open redirect detection

### Security Headers
All responses include:
- `Content-Security-Policy`
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `Strict-Transport-Security`

---

## Code Examples

### Python
```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    json={"email": "user@example.com", "password": "SecurePass123"}
)
token = response.json()["access_token"]

# Upload document
with open("newspaper.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/v1/ocr/extract",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": f},
        data={"engine": "tesseract", "language": "en"}
    )
    
print(response.json()["text"])
```

### JavaScript (Node.js)
```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

// Login
const loginResponse = await axios.post(
    'http://localhost:8000/api/v1/auth/login',
    {
        email: 'user@example.com',
        password: 'SecurePass123'
    }
);
const token = loginResponse.data.access_token;

// Upload document
const form = new FormData();
form.append('file', fs.createReadStream('newspaper.jpg'));
form.append('engine', 'tesseract');
form.append('language', 'en');

const ocrResponse = await axios.post(
    'http://localhost:8000/api/v1/ocr/extract',
    form,
    {
        headers: {
            'Authorization': `Bearer ${token}`,
            ...form.getHeaders()
        }
    }
);

console.log(ocrResponse.data.text);
```

### cURL
```bash
# Login
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123"}' \
  | jq -r '.access_token')

# Upload document
curl -X POST http://localhost:8000/api/v1/ocr/extract \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@newspaper.jpg" \
  -F "engine=tesseract" \
  -F "language=en"
```

---

## Interactive Documentation

Vuva provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to:
- Browse all endpoints
- Try out API calls directly
- See request/response schemas
- Download OpenAPI specification

---

## Support

For issues, questions, or feature requests:
- GitHub Issues: [Repository](https://github.com/your-org/vuva)
- Documentation: `/docs` directory
- API Status: `GET /api/v1/health`

---

**Last Updated**: January 24, 2026  
**API Version**: 1.2.1  
**Documentation Version**: 1.0
