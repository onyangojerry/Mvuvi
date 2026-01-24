# Priority Tasks - Vuva Project

**Date**: January 24, 2026  
**Version**: 1.1.0  
**Status**: Production Preparation Phase

---

## High Priority Tasks 🔴

### 1. Run Pytest Suite and Fix Failures
**Status**: Ready to execute  
**Estimated Time**: 2-3 hours  
**Dependencies**: None

**Tasks**:
- Execute full test suite: `pytest tests/ -v --cov=src --cov-report=html`
- Fix failing tests (currently 26/27 news ingestion tests need alignment)
- Achieve >70% code coverage
- Generate coverage report
- Document test results

**Success Criteria**:
- All tests passing (green)
- Coverage report generated
- No critical failures

---

### 2. Activate JWT Authentication
**Status**: Framework ready, needs activation  
**Estimated Time**: 3-4 hours  
**Dependencies**: None

**Tasks**:
- Create authentication middleware
- Implement login endpoint (`/api/v1/auth/login`)
- Implement token refresh endpoint (`/api/v1/auth/refresh`)
- Add protected route decorator
- Integrate with existing endpoints
- Add authentication tests

**Implementation Files**:
- `src/api/v1/auth.py` (new)
- `src/middleware/auth.py` (new)
- `src/services/auth_service.py` (new)
- `tests/test_auth.py` (new)

**Success Criteria**:
- JWT tokens generated and validated
- Protected endpoints require authentication
- Token refresh mechanism working
- Tests passing

---

### 3. Set Up GitHub Actions CI/CD
**Status**: Not started  
**Estimated Time**: 2-3 hours  
**Dependencies**: Tests passing

**Tasks**:
- Create `.github/workflows/test.yml`
- Create `.github/workflows/deploy.yml`
- Configure automated testing on push
- Add code coverage reporting
- Add linting (ruff, black)
- Configure deployment to staging
- Add status badges to README

**Success Criteria**:
- Tests run automatically on every push
- Coverage reports generated
- Build status visible
- Deployment pipeline functional

---

### 4. Align News Ingestion Tests with Implementation
**Status**: Tests created, need alignment  
**Estimated Time**: 1-2 hours  
**Dependencies**: None

**Tasks**:
- Review actual method signatures in `news_ingestion.py`
- Update test method calls to match implementation
- Add missing test fixtures
- Ensure all 27 tests pass
- Add integration tests

**Files to Update**:
- `tests/test_news_ingestion.py`
- May need to refactor `src/services/news_ingestion.py`

**Success Criteria**:
- All 27 news ingestion tests passing
- Integration tests working
- Coverage >80% for news module

---

## Medium Priority Tasks 🟡

### 1. Create Database Migrations
**Status**: Not started  
**Estimated Time**: 4-6 hours  
**Dependencies**: PostgreSQL installed

**Tasks**:
- Install PostgreSQL locally
- Create database schema design
- Initialize Alembic migrations
- Create migration scripts for:
  - Users table
  - Articles table
  - Sources table
  - API keys table
  - User preferences table
- Create initial data seeds
- Add database connection pooling
- Implement SQLAlchemy models
- Add database tests

**Implementation Files**:
- `alembic/versions/001_initial_schema.py` (new)
- `src/models/user.py` (new)
- `src/models/article.py` (new)
- `src/models/source.py` (new)
- `src/models/api_key.py` (new)
- `src/database.py` (update)
- `tests/test_database.py` (new)

**Success Criteria**:
- Database created and running
- All migrations applied
- Models defined with relationships
- Connection pooling working
- CRUD operations functional
- Tests passing

**Schema Design**:
```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL, -- 'free', 'basic', 'premium', 'admin'
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Articles table
CREATE TABLE articles (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT,
    summary TEXT,
    url TEXT UNIQUE NOT NULL,
    source_id UUID REFERENCES sources(id),
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Sources table
CREATE TABLE sources (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url TEXT NOT NULL,
    category VARCHAR(100),
    feed_type VARCHAR(50), -- 'rss', 'api', 'scrape'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- API Keys table
CREATE TABLE api_keys (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    tier VARCHAR(50) NOT NULL, -- 'free', 'basic', 'premium'
    rate_limit INTEGER NOT NULL,
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

### 2. Add News API Endpoints
**Status**: Service implemented, endpoints needed  
**Estimated Time**: 3-4 hours  
**Dependencies**: None

**Tasks**:
- Create news API router (`/api/v1/news`)
- Implement endpoints:
  - `GET /api/v1/news/sources` - List available sources
  - `GET /api/v1/news/categories` - List categories
  - `GET /api/v1/news/{category}` - Get news by category
  - `GET /api/v1/news/hackernews` - Get Hacker News stories
  - `POST /api/v1/news/extract` - Extract full article
  - `GET /api/v1/news/search` - Search articles
- Add request validation
- Add response pagination
- Add rate limiting
- Add caching
- Add comprehensive tests

**Implementation Files**:
- `src/api/v1/news.py` (new)
- `src/schemas/news.py` (new)
- `tests/test_news_api.py` (new)

**API Endpoints Specification**:

```python
# GET /api/v1/news/sources
Response: {
    "sources": [
        {
            "name": "TechCrunch",
            "url": "https://techcrunch.com/feed/",
            "category": "technology",
            "type": "rss"
        }
    ]
}

# GET /api/v1/news/technology?limit=10&offset=0
Response: {
    "articles": [...],
    "total": 150,
    "page": 1,
    "pages": 15
}

# POST /api/v1/news/extract
Request: {"url": "https://example.com/article"}
Response: {
    "title": "Article Title",
    "text": "Full content...",
    "author": "John Doe",
    "published": "2026-01-24T10:00:00"
}
```

**Success Criteria**:
- All endpoints functional
- Request validation working
- Pagination implemented
- Rate limiting enforced
- Tests passing (>80% coverage)
- API documentation updated

---

### 3. Implement RBAC Authorization
**Status**: Roles defined, implementation needed  
**Estimated Time**: 4-5 hours  
**Dependencies**: Database migrations, JWT authentication

**Tasks**:
- Define permission system
- Create role-based decorators
- Implement role checking middleware
- Add role assignment to users
- Create admin endpoints for role management
- Implement resource-level permissions
- Add authorization tests

**Roles and Permissions**:

```python
ROLES = {
    "free": {
        "permissions": [
            "read:news",
            "read:sources"
        ],
        "rate_limit": 100,  # per hour
    },
    "basic": {
        "permissions": [
            "read:news",
            "read:sources",
            "read:full_articles",
            "write:preferences"
        ],
        "rate_limit": 1000,
    },
    "premium": {
        "permissions": [
            "read:news",
            "read:sources",
            "read:full_articles",
            "write:preferences",
            "read:analytics",
            "unlimited:ocr"
        ],
        "rate_limit": 10000,
    },
    "admin": {
        "permissions": ["*"],  # All permissions
        "rate_limit": None,  # No limit
    }
}
```

**Implementation Files**:
- `src/middleware/authorization.py` (new)
- `src/services/permission_service.py` (new)
- `src/api/v1/admin.py` (new)
- `tests/test_authorization.py` (new)

**Decorators**:
```python
@require_role("premium")
@require_permission("read:analytics")
async def get_analytics():
    ...
```

**Success Criteria**:
- Role system functional
- Permission checks working
- Admin endpoints protected
- Rate limiting by role
- Tests passing
- Documentation updated

---

### 4. Add Monitoring and Logging
**Status**: Basic logging exists, needs enhancement  
**Estimated Time**: 3-4 hours  
**Dependencies**: None

**Tasks**:
- Implement structured logging (structlog)
- Add request/response logging middleware
- Create custom logger configuration
- Add log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Implement log rotation
- Add performance metrics
- Create health check dashboard
- Add error tracking
- Implement audit logging for security events

**Implementation Files**:
- `src/middleware/logging.py` (new)
- `src/utils/logger.py` (new)
- `src/monitoring/metrics.py` (new)
- `src/monitoring/health.py` (update)
- `logs/` directory structure (new)

**Logging Structure**:
```python
# Example structured log
{
    "timestamp": "2026-01-24T10:30:00Z",
    "level": "INFO",
    "message": "OCR processing completed",
    "request_id": "req_abc123",
    "user_id": "user_xyz",
    "endpoint": "/api/v1/ocr/extract",
    "method": "POST",
    "status_code": 200,
    "duration_ms": 245,
    "ocr_engine": "tesseract",
    "file_size_kb": 1024
}
```

**Monitoring Endpoints**:
- `GET /api/v1/metrics` - Prometheus-compatible metrics
- `GET /api/v1/health/detailed` - Detailed health status
- `GET /api/v1/logs` - Recent logs (admin only)

**Metrics to Track**:
- Request count by endpoint
- Response times (p50, p95, p99)
- Error rates
- OCR processing times
- Database query times
- Cache hit/miss rates
- Active users
- Rate limit hits

**Success Criteria**:
- Structured logging working
- Log rotation configured
- Metrics collection active
- Health dashboard functional
- Performance tracking working
- Audit logs for security events
- Tests passing

---

## Low Priority Tasks 🟢

### 1. Frontend Development
**Status**: Not started  
**Estimated Time**: 2-3 weeks  
**Dependencies**: All API endpoints complete

**Tasks**:
- Set up Next.js project
- Create UI components
- Implement authentication flow
- Build news feed interface
- Add OCR upload interface
- Create user dashboard
- Implement real-time updates

---

### 2. Redis Caching Implementation
**Status**: Configured, not active  
**Estimated Time**: 2-3 hours  
**Dependencies**: Redis server installed

---

### 3. Docker Containerization
**Status**: Not started  
**Estimated Time**: 3-4 hours  
**Dependencies**: None

---

### 4. Kubernetes Deployment
**Status**: Not started  
**Estimated Time**: 1 week  
**Dependencies**: Docker, production infrastructure

---

## Task Dependencies Graph

```
High Priority:
  1. Pytest Suite → (independent)
  2. JWT Auth → (independent)
  3. CI/CD → (requires: 1)
  4. Test Alignment → (independent)

Medium Priority:
  1. Database → (independent)
  2. News API → (independent)
  3. RBAC → (requires: 1, 2 from High)
  4. Monitoring → (independent)

Low Priority:
  1. Frontend → (requires: all Medium)
  2. Redis → (independent)
  3. Docker → (independent)
  4. Kubernetes → (requires: 3)
```

---

## Implementation Order (Recommended)

**Phase 1 - High Priority** (1-2 days):
1. Run and fix tests
2. Align news ingestion tests
3. Activate JWT authentication
4. Set up CI/CD

**Phase 2 - Medium Priority** (2-3 days):
1. Create database migrations
2. Add news API endpoints
3. Implement RBAC authorization
4. Add monitoring and logging

**Phase 3 - Low Priority** (1-2 weeks):
1. Redis caching
2. Docker containerization
3. Frontend development
4. Kubernetes deployment

---

## Success Metrics

### By End of Phase 2:
- ✅ All tests passing (100%)
- ✅ Code coverage >80%
- ✅ CI/CD pipeline active
- ✅ Database fully operational
- ✅ Authentication & authorization complete
- ✅ Monitoring and logging implemented
- ✅ All API endpoints documented
- ✅ Production-ready status: 95%

### Production Readiness Checklist:
- [ ] All tests passing
- [ ] Security audit complete
- [ ] Performance benchmarks met
- [ ] Documentation complete
- [ ] Monitoring active
- [ ] Backup strategy in place
- [ ] Disaster recovery plan
- [ ] Load testing completed
- [ ] SSL/TLS configured
- [ ] Rate limiting enforced

---

**Last Updated**: January 24, 2026  
**Next Review**: After Phase 2 completion
