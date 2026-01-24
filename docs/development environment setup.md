# Development Environment Setup

## Prerequisites

### Required Software [Done] VERIFIED
- **Python 3.9+**: [Done] For backend API and ML components
- **Git**: [Done] Version control
- **Tesseract OCR**: [Done] Required for OCR functionality
  - macOS: `brew install tesseract`
  - Ubuntu: `apt-get install tesseract-ocr`
  - Windows: Download installer from GitHub

### Optional Software
- **Docker**: For containerization (not yet used)
- **PostgreSQL 14+**: Database (configured but not installed)
- **Redis**: Caching layer (configured but not installed)
- **Node.js 18+**: For frontend (not started)

### Development Tools
- **IDE**: VS Code (recommended)
- **API Testing**: Built-in Swagger UI at /docs [Done]

## Installation Steps [Done] COMPLETED

### 1. Project Setup
```bash
# Navigate to project
cd /Users/loan/Desktop/Mvuvi/vuva

# Project structure already created [Done]
```

### 2. Python Environment [Done]
```bash
# Virtual environment already created at:
# /Users/loan/Desktop/Mvuvi/vuva/venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows

# Dependencies already installed [Done]
# See requirements.txt for full list
```

### 3. Environment Configuration [Done]
```bash
# .env file already configured [Done]
# Located at: /Users/loan/Desktop/Mvuvi/vuva/.env

# Key settings:
# - DATABASE_URL: PostgreSQL connection (pending DB installation)
# - REDIS_URL: Redis connection (pending Redis installation)
# - OCR_ENGINE: tesseract (default)
# - DEBUG: True (development mode)
```

### 4. Install Tesseract OCR [Done]
```bash
# macOS
brew install tesseract

# Verify installation
tesseract --version
# Should show: tesseract 5.x.x
```

### 5. Database Setup [Urgent] PENDING
```bash
# PostgreSQL not yet installed
# When ready:
# brew install postgresql@15  # macOS
# brew services start postgresql@15

# Create database:
# createdb newspaper_db

# Run migrations (when created):
# alembic upgrade head
```

### 6. Redis Setup [Urgent] PENDING
```bash
# Redis not yet installed
# When ready:
# brew install redis  # macOS
# brew services start redis
```

## Running the Application

### Development Mode [Done] WORKING

**Method 1: Direct Python (Recommended)**
```bash
# From project root: /Users/loan/Desktop/Mvuvi/vuva
cd /Users/loan/Desktop/Mvuvi/vuva

# Using venv Python directly
/Users/loan/Desktop/Mvuvi/vuva/venv/bin/python -m src.main

# Or activate venv first
source venv/bin/activate
python -m src.main
```

**Method 2: With Environment Variables**
```bash
cd /Users/loan/Desktop/Mvuvi/vuva
PYTHONPATH=/Users/loan/Desktop/Mvuvi/vuva venv/bin/python -m src.main
```

**Access Points** [Done]:
- **API**: http://localhost:8000 or http://0.0.0.0:8000
- **Interactive Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Background Services [Urgent] NOT YET IMPLEMENTED
```bash
# PostgreSQL (when installed)
# brew services start postgresql@15

# Redis (when installed)
# brew services start redis

# Worker processes (future)
# celery -A app worker -l info
```

### Docker Compose [Urgent] NOT YET CONFIGURED
```bash
# Future implementation
# docker-compose up
```

## Configuration

### Environment Variables
```env
# API Configuration
API_HOST=localhost
API_PORT=8000
SECRET_KEY=your-secret-key

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/newsdb

# OCR Service
OCR_ENGINE=tesseract
OCR_LANGUAGES=eng,fra,spa

# Neural Network
MODEL_PATH=./models/error_correction.pt
BATCH_SIZE=32

# Real-time Feed
REDIS_URL=redis://localhost:6379
WEBSOCKET_PORT=3001
```

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

**Database Connection Error**
- Verify PostgreSQL is running: `docker ps`
- Check DATABASE_URL in .env

**OCR Not Working**
- Install Tesseract: `brew install tesseract` (macOS)
- Verify installation: `tesseract --version`

**Model Loading Error**
- Ensure models are downloaded: `ls models/`
- Re-run download script if needed
