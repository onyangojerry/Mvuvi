# Vuva - Newspaper Ingestion API

> Lightweight API system for newspaper ingestion with OCR, AI processing, and personalized news feeds using novel randomization algorithms

![Status](https://img.shields.io/badge/status-development-yellow)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🚀 Quick Start

```bash
# Navigate to project
cd /Users/loan/Desktop/Mvuvi/vuva

# Activate virtual environment
source venv/bin/activate

# Run the API
python -m src.main

# Access API documentation
open http://localhost:8000/docs
```

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [OCR Engines](#ocr-engines)
- [Development](#development)
- [Testing](#testing)
- [Documentation](#documentation)
- [Roadmap](#roadmap)

## 🎯 Overview

Vuva is a specialized newspaper ingestion system that combines:
- **Multi-engine OCR** for accurate text extraction from newspaper images
- **Novel randomization algorithms** for personalized news recommendations
- **Lightweight FastAPI** framework for high-performance async operations
- **AI-powered processing** with neural networks and agentic systems

### Current Status

✅ **Operational**: Core API, OCR with 3 engines, Image preprocessing  
🔄 **In Progress**: Database integration, News feed algorithms  
📋 **Planned**: Neural network error correction, Real-time WebSocket feed, Frontend UI

## ✨ Features

### Implemented ✅

- **FastAPI Framework** - High-performance async web framework
- **Multi-Engine OCR** - Three OCR engines for robust text extraction:
  - Tesseract OCR (fast, reliable)
  - EasyOCR (deep learning, complex layouts)
  - PaddleOCR (mobile-optimized, Asian languages)
- **Image Preprocessing** - Advanced image enhancement pipeline
- **Lazy Loading** - Efficient memory management for ML libraries
- **Interactive Docs** - Swagger UI and ReDoc
- **CORS & Compression** - Production-ready middleware
- **Environment Config** - Pydantic-based settings management
- **File Upload** - Multi-part form data with validation
- **Batch Processing** - Process multiple images concurrently

### In Development 🔄

- **PostgreSQL Database** - Configured, pending implementation
- **Redis Caching** - For performance optimization
- **JWT Authentication** - Secure API access
- **Rate Limiting** - API usage controls
- **News Feed API** - Personalized feed delivery

### Planned 📋

- **Neural Network** - OCR error correction model
- **Randomization Algorithms** - Novel personalization system
- **WebSocket Streaming** - Real-time news feed
- **Agentic Systems** - AI-powered content analysis
- **Frontend UI** - React-based news reader

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Client Applications             │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│          FastAPI Server                 │
│  ┌────────────┐  ┌──────────────────┐  │
│  │Health Check│  │  OCR Service     │  │
│  └────────────┘  │  - Tesseract     │  │
│  ┌────────────┐  │  - EasyOCR       │  │
│  │Ingest API  │  │  - PaddleOCR     │  │
│  └────────────┘  └──────────────────┘  │
│  ┌────────────┐  ┌──────────────────┐  │
│  │Feed API    │  │Image Preprocessor│  │
│  └────────────┘  └──────────────────┘  │
└─────────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│         Data Layer (Planned)            │
│  ┌──────────┐  ┌────────┐  ┌────────┐  │
│  │PostgreSQL│  │ Redis  │  │   S3   │  │
│  └──────────┘  └────────┘  └────────┘  │
└─────────────────────────────────────────┘
```

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- Tesseract OCR
- Virtual environment (recommended)

### Install Tesseract

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

### Setup Project

```bash
# Clone or navigate to project
cd /Users/loan/Desktop/Mvuvi/vuva

# Activate virtual environment (already created)
source venv/bin/activate

# All dependencies already installed
# See requirements.txt for full list

# Verify installation
python -c "import fastapi, pytesseract; print('✅ Ready')"
```

### Environment Configuration

The `.env` file is already configured with defaults:

```env
# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Database (not yet installed)
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/newspaper_db

# Redis (not yet installed)
REDIS_URL=redis://localhost:6379/0

# OCR Settings
OCR_ENGINE=tesseract
OCR_LANGUAGES=eng
OCR_TIMEOUT_SECONDS=30
MAX_IMAGE_SIZE_MB=10
```

## 🎮 Usage

### Starting the Server

```bash
# Method 1: Direct execution
cd /Users/loan/Desktop/Mvuvi/vuva
python -m src.main

# Method 2: With uvicorn directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Access Points

- **API Root**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

### Basic OCR Example

```python
import requests

# Upload an image for OCR
with open('newspaper.jpg', 'rb') as f:
    files = {'file': f}
    data = {'engine': 'tesseract', 'language': 'eng'}
    response = requests.post(
        'http://localhost:8000/api/v1/ocr/extract',
        files=files,
        data=data
    )
    
result = response.json()
print(f"Extracted text: {result['data']['text']}")
print(f"Confidence: {result['data']['confidence']}")
```

### Compare OCR Engines

```python
# Compare all three OCR engines
with open('newspaper.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/api/v1/ocr/extract/compare',
        files=files
    )
    
results = response.json()
for engine, result in results['data'].items():
    print(f"{engine}: {result['confidence']:.2%} confidence")
```

## 🔌 API Endpoints

### Health & Status

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/` | API information | ✅ |
| GET | `/health` | Health check | ✅ |
| GET | `/api/v1/health` | Detailed health | ✅ |

### OCR Processing

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/v1/ocr/extract` | Extract text from image | ✅ |
| POST | `/api/v1/ocr/extract/compare` | Compare all engines | ✅ |
| POST | `/api/v1/ocr/extract/batch` | Batch processing | ✅ |
| GET | `/api/v1/ocr/engines` | List available engines | ✅ |

### Newspaper Ingestion

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| POST | `/api/v1/ingest/upload` | Upload newspaper image | ✅ Structure |
| POST | `/api/v1/ingest/batch` | Batch upload | ✅ Structure |
| GET | `/api/v1/ingest/status/{id}` | Check status | 🔄 Pending DB |
| GET | `/api/v1/ingest/history` | Upload history | 🔄 Pending DB |

### News Feed

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/api/v1/feed` | Get news feed | ✅ Structure |
| GET | `/api/v1/feed/stream` | WebSocket stream | 📋 Planned |
| POST | `/api/v1/feed/preferences` | Update preferences | 📋 Planned |
| GET | `/api/v1/feed/article/{id}` | Get article | 📋 Planned |

## 🔍 OCR Engines

### Tesseract OCR ✅

**Best for**: Standard printed text, high speed  
**Languages**: 100+ languages  
**Performance**: ~1-3 seconds per image  
**Accuracy**: Good for clean text

```python
# Usage
POST /api/v1/ocr/extract
{
    "engine": "tesseract",
    "language": "eng"
}
```

### EasyOCR ✅

**Best for**: Complex layouts, handwriting, 80+ languages  
**Languages**: 80+ including Asian languages  
**Performance**: ~3-8 seconds (first load + processing)  
**Accuracy**: Excellent for difficult images

```python
# Usage
POST /api/v1/ocr/extract
{
    "engine": "easyocr",
    "language": "en"
}
```

### PaddleOCR ✅

**Best for**: Asian languages, mobile deployment  
**Languages**: Chinese, Japanese, Korean, English  
**Performance**: ~2-5 seconds  
**Accuracy**: Excellent for CJK languages

```python
# Usage
POST /api/v1/ocr/extract
{
    "engine": "paddleocr",
    "language": "en"
}
```

## 🛠️ Development

### Project Structure

```
vuva/
├── src/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── api/
│   │   └── v1/
│   │       ├── health.py    # Health endpoints
│   │       ├── ingest.py    # Ingestion endpoints
│   │       ├── feed.py      # Feed endpoints
│   │       └── ocr.py       # OCR endpoints
│   └── services/
│       ├── ocr_service.py   # OCR service
│       └── news_ingestion.py # News service
├── tests/                   # Unit tests
├── docs/                    # Documentation
├── addr/                    # Standards & guidelines
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
└── README.md               # This file
```

### Adding New Endpoints

```python
# src/api/v1/my_endpoint.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/my-route")
async def my_handler():
    return {"status": "success"}
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_ocr.py
```

## 📚 Documentation

Comprehensive documentation available in the `docs/` folder:

- **[Project Status](docs/project%20status.md)** - Current implementation status
- **[API Architecture](docs/api%20architecture.md)** - System design and data flow
- **[Technology Stack](docs/technology%20stack.md)** - Technologies and versions
- **[Development Environment](docs/development%20environment%20setup.md)** - Setup guide
- **[Development Timeline](docs/development%20timeline.md)** - Project phases
- **[Comprehensive Audit](docs/comprehensive%20audit.md)** - Detailed system audit
- **[Algorithm Research](docs/algorithm%20research.md)** - Randomization algorithms
- **[Improvement Roadmap](docs/improvement%20roadmap.md)** - Future enhancements

### Standards & Guidelines

Located in `addr/` folder:

- **[API Standards](addr/API%20standards.md)** - API design guidelines
- **[Security Standards](addr/security%20standards.md)** - Security practices
- **[Team Roles](addr/team%20roles.md)** - Team structure
- **[Workflow](addr/workflow.md)** - Development workflow

## 🗺️ Roadmap

### Phase 1: Foundation ✅ COMPLETE
- [x] FastAPI framework setup
- [x] Core API endpoints
- [x] OCR engine integration (3 engines)
- [x] Image preprocessing pipeline
- [x] Documentation structure

### Phase 2: Data Layer 🔄 IN PROGRESS
- [ ] PostgreSQL database setup
- [ ] Database models and migrations
- [ ] Redis caching implementation
- [ ] News source integration (RSS, APIs)
- [ ] Authentication with JWT

### Phase 3: Intelligence 📋 PLANNED
- [ ] Neural network error correction
- [ ] Randomization algorithms implementation
- [ ] Agentic systems integration
- [ ] Content analysis and classification
- [ ] Advanced personalization

### Phase 4: Real-time & Frontend 📋 PLANNED
- [ ] WebSocket implementation
- [ ] Real-time news feed
- [ ] Frontend application (React)
- [ ] User dashboard
- [ ] Mobile responsive design

### Phase 5: Production 📋 PLANNED
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Monitoring and observability
- [ ] Load testing
- [ ] Security hardening
- [ ] Production deployment

## 🔧 Configuration

### Key Settings

```python
# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
DEBUG = True  # Set to False in production

# OCR Settings
OCR_ENGINE = "tesseract"  # tesseract | easyocr | paddleocr
OCR_LANGUAGES = "eng"
OCR_TIMEOUT_SECONDS = 30
MAX_IMAGE_SIZE_MB = 10

# Security
SECRET_KEY = "your-secret-key"  # Change in production!
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
```

## 🤝 Contributing

Currently in development phase. Contribution guidelines coming soon.

## 📄 License

MIT License - see LICENSE file for details

## 👥 Team

See [Team Roles](addr/team%20roles.md) for current team structure.

## 📞 Support

For issues and questions:
- Check the [documentation](docs/)
- Review API docs at `/docs` endpoint
- See troubleshooting guides (coming soon)

## 🏆 Acknowledgments

- FastAPI framework by Sebastián Ramírez
- Tesseract OCR by Google
- EasyOCR by JaidedAI
- PaddleOCR by PaddlePaddle

---

**Built with ❤️ using FastAPI and Python**

*Last Updated: January 24, 2026*
