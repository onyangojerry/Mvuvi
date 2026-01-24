# Vuva - Newspaper Ingestion API

> Lightweight FastAPI system for newspaper ingestion with multi-engine OCR, AI processing, and personalized news feeds

![Status](https://img.shields.io/badge/status-development-yellow)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🚀 Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run the API
python -m src.main

# Access interactive docs
open http://localhost:8000/docs
```

## 🎯 What is Vuva?

Vuva extracts text from newspaper images using three OCR engines (Tesseract, EasyOCR, PaddleOCR) and delivers personalized news feeds through novel randomization algorithms. Built with FastAPI for high-performance async operations.

**Current Status:** Core API operational with OCR processing. Database and authentication in progress.


## ✨ Key Features

- **Multi-Engine OCR**: Tesseract, EasyOCR, PaddleOCR with lazy-loading
- **FastAPI Framework**: Async, type-safe, with auto-generated OpenAPI docs
- **Image Preprocessing**: Grayscale, denoise, threshold pipeline
- **Batch Processing**: Handle multiple images concurrently
- **RESTful API**: Versioned endpoints with proper HTTP methods

## 📦 Installation

### Prerequisites
- Python 3.9+
- Tesseract OCR: `brew install tesseract` (macOS) or `apt-get install tesseract-ocr` (Linux)

### Setup
```bash
# Install dependencies (already done if using existing venv)
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # Edit as needed

# Verify setup
python -c "import fastapi, pytesseract; print('✅ Ready')"
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/docs` | GET | Interactive API documentation |
| `/health` | GET | Health check |
| `/api/v1/ocr/extract` | POST | Extract text from image |
| `/api/v1/ocr/extract/compare` | POST | Compare all OCR engines |
| `/api/v1/feed` | GET | Get news feed |

**See full API reference:** [API Architecture](docs/api%20architecture.md)

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](docs/development%20environment%20setup.md) | Detailed setup instructions |
| [API Architecture](docs/api%20architecture.md) | System design and endpoints |
| [Technology Stack](docs/technology%20stack.md) | Technologies and versions |
| [Roadmap](docs/roadmap.md) | Development phases and timeline |
| [Project Status](docs/project%20status.md) | Current implementation status |
| [Contributing Guide](docs/CONTRIBUTING.md) | How to contribute |

**Standards:** [API Standards](addr/API%20standards.md) • [Security](addr/security%20standards.md) • [Workflow](addr/workflow.md)

## 🛠️ Development

```bash
# Run tests (when pytest is installed)
pytest tests/ -v

# Start with hot-reload
uvicorn src.main:app --reload

# Project structure
src/
├── api/v1/          # API endpoints
├── services/        # Business logic
└── config.py        # Configuration
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `pytest tests/`
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Open a Pull Request

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🏆 Acknowledgments

Built with [FastAPI](https://fastapi.tiangolo.com/), [Tesseract OCR](https://github.com/tesseract-ocr/tesseract), [EasyOCR](https://github.com/JaidedAI/EasyOCR), and [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)

---

**Grade:** B+ (85/100) • **Status:** Development • **Version:** 1.0.0

*For detailed technical assessment, see [AGILE_SWE_ASSESSMENT.md](docs/AGILE_SWE_ASSESSMENT.md)*

