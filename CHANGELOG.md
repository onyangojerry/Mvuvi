# 2026-01-31
- Fix: Celery worker now imports `src.tasks.ocr` to register OCR tasks for user-uploaded images.
- Fix: Feed API uses correct method to count articles, resolving AttributeError.
- Feature: WebSocket endpoint subscribes to Redis and broadcasts new articles in real time to all clients.
- Fix: Frontend WebSocket handler (`useNewsStream.ts`) now uses `message.article` for real-time updates.
- Docs: Updated `ocr_pipeline.md` with full, up-to-date documentation of the OCR-to-newsfeed pipeline, real-time updates, and troubleshooting.
- Logging: Ingestion endpoint now logs and returns detailed tracebacks for easier debugging.
# Vuva Project Changelog

All notable changes to the Vuva Newspaper Ingestion API project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### In Progress
- File storage implementation (local filesystem + S3-compatible)
- Queue processing for OCR jobs
- Async test conversion for remaining test suites

### Planned
- Neural network OCR error correction
- WebSocket real-time feed streaming
- Frontend React application

---

## [1.2.1] - 2026-01-24

### Added - Security Implementation Complete ✅

#### Comprehensive Security Module (100% Test Coverage)
- **Input Sanitization** (11 tests passing)
  - XSS prevention (script tags, event handlers, javascript: protocol)
  - Command injection protection (shell metacharacters)
  - Unicode normalization (fullwidth character attacks)
  - SQL injection patterns detection
  - Null byte injection prevention
- **File Upload Validation** (11 tests passing)
  - Type validation with whitelist
  - Double extension detection (file.pdf.exe)
  - Size limit enforcement (configurable, default 10MB)
  - Case-insensitive validation
- **Path Traversal Prevention** (8 tests passing)
  - Parent directory traversal (../)
  - Absolute path detection (Unix & Windows)
  - URL-encoded traversal attempts
  - Filename sanitization with Unicode support
- **URL Validation** (10 tests passing)
  - Protocol whitelist (http/https only)
  - Dangerous protocol blocking (javascript:, data:, file:)
  - Open redirect pattern detection
  - Malformed URL rejection
- **SQL Injection Prevention** (5 tests passing)
  - Basic injection pattern removal
  - UNION attack detection
  - Comment injection prevention
  - Time-based injection detection
  - Hex encoding attempts
- **Security Headers & Rate Limiting** (3 tests passing)
  - CSP, X-Frame-Options, X-Content-Type-Options
  - CORS configuration
  - Tiered rate limits (100/1000/10000 per hour)
- **Data Validation Helpers** (3 tests passing)
  - Email format validation
  - UUID format validation
  - Password strength requirements

#### Test Infrastructure Improvements
- Fixed async/await patterns in test fixtures
- Rewrote `tests/conftest.py` with proper AsyncClient support
- In-memory SQLite database with automatic setup/teardown
- Dependency override pattern for database sessions
- Authenticated client fixture with JWT tokens
- Authentication tests improved from 10/27 to 20/27 passing

#### Documentation Updates
- Created `docs/TEST_FIX_SUMMARY.md` - Test infrastructure fix details
- Created `docs/PRODUCTION_STATUS_UPDATE.md` - Current status and next steps
- Updated all production readiness documentation

#### Security Functions Implemented
```python
# New security functions in src/security.py
sanitize_input()           # Enhanced XSS & command injection protection
sanitize_filename()        # Path traversal prevention
sanitize_sql_input()       # SQL injection defense-in-depth
validate_file_type()       # Extension validation with double-extension check
check_file_size()          # Size validation
validate_file_upload()     # Comprehensive upload validation
prevent_path_traversal()   # Path safety with URL decoding
validate_url()             # URL protocol & pattern validation
```

### Fixed
- Async/sync mismatch in test fixtures causing 42 test failures
- UUID serialization error in authentication responses
- Duplicate fixture definitions in test_authentication.py
- Test isolation issues with password hashing

### Dependencies Added
- `slowapi` - For rate limiting functionality

### Test Results
```
Total Tests: 164
Passing: 100 (61%)
Security: 51/51 (100%) ✅
Cache: 25/25 (100%) ✅
Authentication: 20/27 (74%)
Other suites: Need async conversion
```

---

## [1.2.0] - 2026-01-24

### Added - Critical Features Activation

#### Enterprise Authentication System
- **Argon2id Password Hashing** (OWASP recommended, Password Hashing Competition winner)
  - Memory-hard algorithm (64MB) resistant to GPU/ASIC attacks
  - Configurable: 3 iterations, 4 parallel threads, 32-byte hash output
  - Timing-attack resistant verification
  - Automatic password rehashing when parameters updated
- **JWT Token System**
  - Access tokens (15-minute expiry) for API access
  - Refresh tokens (7-day expiry) for token rotation
  - Secure token generation using Python secrets module
  - JWT ID (jti) for potential token revocation
  - RS256 algorithm for token signing
- **Authentication Endpoints** (8 total):
  - `POST /api/v1/auth/register` - User registration with password validation
  - `POST /api/v1/auth/login` - Login with JWT access + refresh tokens
  - `POST /api/v1/auth/refresh` - Token refresh mechanism
  - `GET /api/v1/auth/me` - Get current authenticated user
  - `POST /api/v1/auth/change-password` - Secure password change
  - `POST /api/v1/auth/api-keys` - Generate API keys for programmatic access
  - `GET /api/v1/auth/api-keys` - List user's API keys
  - `DELETE /api/v1/auth/api-keys/:id` - Revoke API key
- **Password Requirements**:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
- **Security Features**:
  - API keys hashed in database (never stored in plain text)
  - Timing-attack resistant password comparisons
  - Email validation with dns verification
  - User role system (free, basic, premium, admin)
  - Rate limiting by user tier

#### Database & Infrastructure
- **PostgreSQL Database Fully Operational**
  - Dedicated `vuva_app` database user created
  - Proper privilege isolation and security
  - 7 database tables created via Alembic migrations:
    - `users` - User authentication and roles
    - `sources` - News sources (RSS, API, scrape)
    - `articles` - News articles with full metadata
    - `api_keys` - API key management with rate limiting
    - `user_preferences` - User settings and preferences
    - `audit_logs` - Security audit trail
    - `ocr_jobs` - OCR job tracking and performance
  - Async database support with asyncpg + greenlet
  - Connection pooling (20 connections)
  - Alembic migrations configured for schema versioning
- **Database Features**:
  - UUID primary keys for all tables
  - Automatic timestamps (created_at, updated_at)
  - Foreign key relationships with cascading
  - Optimized indexes for common queries
  - JSON support for flexible metadata storage

#### Middleware & Monitoring Integration
- **Logging Middleware**
  - Request ID generation (UUID) for tracking
  - Duration tracking for all requests
  - Client IP extraction
  - Response headers: X-Request-ID, X-Process-Time
  - Structured JSON logging to `logs/app.log`
- **Metrics Middleware**
  - Prometheus-compatible metrics collection
  - Request count by endpoint, method, and status
  - Request duration histograms
  - OCR processing time tracking
  - Database operation duration
  - Cache hit/miss rates
  - Active users tracking
  - API error counting
- **Monitoring Endpoints**:
  - `GET /metrics` - Prometheus metrics endpoint
  - Full integration with monitoring stack

#### News API Activation
- **News API Endpoints** (7 endpoints):
  - `GET /api/v1/news/sources` - List all news sources
  - `GET /api/v1/news/categories` - List news categories
  - `GET /api/v1/news/{category}` - Get news by category (paginated)
  - `GET /api/v1/news/hackernews/top` - Hacker News top stories
  - `POST /api/v1/news/extract` - Full article extraction
  - `POST /api/v1/news/search` - Search articles (placeholder)
  - `GET /api/v1/news/all` - Get news from all categories
- **Features**:
  - Permission-based access control integration ready
  - Request validation with Pydantic schemas
  - Pagination support (limit, offset)
  - Error handling with proper HTTP exceptions
  - Metrics tracking integrated

### Changed
- **Database Configuration**
  - Moved from default PostgreSQL user to dedicated `vuva_app` user
  - Updated DATABASE_URL in .env for proper security isolation
  - Fixed Alembic async/sync URL conversion for migrations
- **Main Application**
  - Integrated all new middleware (logging, metrics)
  - Added database initialization in lifespan
  - Setup structured logging on startup
  - Removed emojis from startup messages for clean logs
- **Models**
  - Fixed SQLAlchemy reserved keyword issue (metadata → extra_data)
  - All models follow async pattern with proper relationships

### Dependencies Added
- `argon2-cffi==25.1.0` - Argon2id password hashing
- `passlib==1.7.4` - Password hashing utilities
- `python-jose==3.5.0` - JWT token handling
- `bcrypt==5.0.0` - Bcrypt support for passlib
- `cryptography==46.0.3` - Cryptographic operations
- `email-validator==2.3.0` - Email validation with DNS
- `asyncpg==0.31.0` - Async PostgreSQL driver
- `psycopg2-binary==2.9.11` - Sync PostgreSQL driver (for Alembic)
- `greenlet==3.2.4` - Async support for SQLAlchemy
- `prometheus-client==0.24.1` - Metrics collection
- `structlog==25.5.0` - Structured logging

### Fixed
- Database connection using correct user credentials
- Alembic migration async/sync URL conversion
- News ingestion service undefined client reference
- News router duplicate prefix issue
- SQLAlchemy metadata column reserved keyword
- Authentication middleware JWT verification

### Security
- Implemented industry-standard Argon2id password hashing
- Added timing-attack resistant authentication
- Created dedicated database user with proper privileges
- API key hashing in database
- Secure random token generation
- Email validation to prevent invalid registrations

---

## [1.1.0] - 2026-01-24

### Added
- **Fast Transcription Endpoint** (`/api/v1/ocr/transcribe-fast`)
  - Optimized for speed with ~100-300ms response time
  - Skips preprocessing for immediate results
  - Minimal JSON response format
  - Perfect for real-time applications
- **Free News Ingestion Service**
  - RSS feed aggregator with 15+ sources across 5 categories
  - Hacker News API integration
  - Full article extraction with newspaper3k
  - Support for technology, world, business, science, and general news
- **Comprehensive Test Suite** (`tests/test_ocr.py`)
  - 25+ test cases covering all OCR functionality
  - Security validation tests
  - Performance benchmarks
  - Error handling tests
  - Batch processing tests
- **Security Module** (`src/security.py`)
  - Input sanitization and validation
  - API key authentication system
  - Security headers middleware
  - Rate limiting by tier
  - Security event logging
- **Documentation**
  - Fast transcription guide with examples
  - Security implementation documentation
  - Comprehensive changelog (this file)

### Changed
- Removed all emojis from documentation for better accessibility
- Updated README from 485 lines to ~150 lines for clarity
- Enhanced roadmap with 5-phase development plan
- Improved project status tracking

### Fixed
- Tesseract OCR installation and configuration
- Image preprocessing pipeline optimization
- Error handling in OCR service

### Security
- Implemented input sanitization for filenames
- Added file content validation with magic bytes
- Path traversal attack prevention
- SQL injection protection in parameters
- Security headers (X-Frame-Options, CSP, etc.)
- Rate limiting infrastructure

---

## [1.0.0] - 2026-01-23

### Added
- **Core API Infrastructure**
  - FastAPI 0.109.0 framework setup
  - Uvicorn 0.27.0 ASGI server
  - Environment-based configuration with Pydantic
  - CORS middleware
  - GZip compression
  - Global exception handling
- **OCR System**
  - Tesseract OCR integration (pytesseract 0.3.10)
  - EasyOCR integration (1.7.1 with PyTorch 2.8.0)
  - PaddleOCR integration (2.7.3 with PaddlePaddle 2.6.0)
  - Lazy-loading pattern for ML libraries
  - Image preprocessing pipeline
    - Grayscale conversion
    - Noise reduction (Gaussian blur)
    - Adaptive thresholding
    - Contrast enhancement
  - Multi-engine comparison endpoint
  - Batch processing support
- **API Endpoints** (10 total)
  - `GET /` - API information
  - `GET /health` - Health check
  - `GET /api/v1/health` - Detailed health check
  - `POST /api/v1/ocr/extract` - Single image OCR
  - `POST /api/v1/ocr/extract/compare` - Compare all engines
  - `POST /api/v1/ocr/extract/batch` - Batch processing
  - `GET /api/v1/ocr/engines` - List available engines
  - `POST /api/v1/ingest/upload` - Upload newspaper image
  - `POST /api/v1/ingest/batch` - Batch upload
  - `GET /api/v1/feed` - Get news feed (structure)
- **Documentation** (12 files)
  - Comprehensive README
  - API architecture documentation
  - Technology stack documentation
  - Development environment setup guide
  - Project status tracking
  - Roadmap with 5 phases
  - Agile SWE assessment (Grade: B+ 85/100)
  - Algorithm research
  - Standards documentation (4 files in addr/)
- **Infrastructure**
  - Git repository initialization
  - GitHub integration (https://github.com/onyangojerry/Mvuvi.git)
  - .gitignore for Python projects
  - requirements.txt with 62 dependencies
  - Virtual environment setup
  - Environment configuration (.env)
- **Testing Framework**
  - pytest configuration
  - Test fixtures
  - 4 test files (health, ingestion, feed, OCR)
  - TestClient setup

### Configuration
- PostgreSQL configured (asyncpg driver)
- Redis configured (not yet running)
- JWT settings prepared
- Rate limiting configured
- OCR engine settings
- File upload limits (10MB)

---

## [0.1.0] - 2026-01-17

### Added
- Initial project structure
- Documentation framework
- Development roadmap
- Technology research
- Standards and guidelines

---

## Version History Summary

| Version | Date | Description | Lines of Code | API Endpoints | Status |
|---------|------|-------------|---------------|---------------|--------|
| 1.1.0 | 2026-01-24 | Fast transcription + News ingestion | ~8,500 | 11 | Current |
| 1.0.0 | 2026-01-23 | Core API + OCR system | ~7,053 | 10 | Stable |
| 0.1.0 | 2026-01-17 | Initial project setup | ~500 | 0 | Archived |

---

## Migration Notes

### Upgrading from 1.0.0 to 1.1.0

**New Dependencies:**
```bash
pip install feedparser newspaper3k python-dateutil beautifulsoup4 slowapi
```

**New Environment Variables:**
```env
# Optional - defaults work for most cases
NEWS_API_ENABLED=True
RSS_FEEDS_ENABLED=True
```

**New Endpoints Available:**
- `POST /api/v1/ocr/transcribe-fast` - Fast transcription
- `GET /api/v1/news/sources` - List news sources (when implemented)
- `GET /api/v1/news/categories` - List categories (when implemented)

**Breaking Changes:**
- None - fully backward compatible

**Deprecated:**
- None yet

---

## Known Issues

### Current (1.1.0)
- PostgreSQL database not yet implemented
- Redis caching not active
- JWT authentication not implemented
- Rate limiting configured but not enforced
- Tests require `pytest` installation
- Some news sources may be unreliable

### Workarounds
- Use in-memory storage for testing
- API accessible without authentication (development only)
- Install Tesseract manually: `brew install tesseract`

---

## Performance Metrics

### 1.1.0 Benchmarks
- API Startup: ~2 seconds
- Health Check: <50ms
- Fast Transcription: 100-300ms
- Regular OCR: 1-8 seconds (depending on engine)
- News Feed Fetch: 2-5 seconds (15 sources)
- Memory Usage: ~500MB with all OCR engines loaded

### Performance Goals (Phase 5)
- API Response: <100ms (p95)
- OCR Processing: <5 seconds
- Throughput: 1000+ req/s
- Uptime: 99.9%

---

## Security Updates

### 1.1.0 Security Enhancements
- Added input sanitization module
- Implemented filename validation
- Added file content validation with magic bytes
- Security headers middleware
- API key authentication framework
- Security event logging
- Rate limiting infrastructure

### Security Audit Status
- **Grade: C+ (75/100)** - Development phase
- Authentication: Not implemented
- Authorization: Not implemented
- Input Validation: Implemented
- Rate Limiting: Configured
- HTTPS: Not configured
- Encryption: Not configured

---

## Contributors

- **Development Team** - Initial work and ongoing development
- **Technical Review** - Agile SWE assessment

---

## Links

- **GitHub Repository**: https://github.com/onyangojerry/Mvuvi.git
- **Documentation**: [docs/](docs/)
- **API Documentation**: http://localhost:8000/docs (when running)
- **Issue Tracker**: GitHub Issues

---

## Support

For issues, questions, or contributions:
1. Check existing documentation in [docs/](docs/)
2. Review this changelog for recent changes
3. Check the [roadmap](docs/roadmap.md) for planned features
4. Open an issue on GitHub

---

**Note**: This changelog is actively maintained. All significant changes are documented here.
