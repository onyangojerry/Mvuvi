# Critical Tasks Implementation Guide

**Date**: January 24, 2026  
**Priority**: CRITICAL - Must Complete Before Production  
**Estimated Total Time**: 1.5 hours  
**Current Blocker**: New features isolated, database not operational

---

## 🎯 Overview

We have successfully implemented 4 medium priority tasks (database models, news API, RBAC, monitoring) but they are **NOT INTEGRATED** into the application. This document provides step-by-step instructions to activate all new features.

### Current Status:
- ✅ Code implemented: Database, News API, RBAC, Monitoring
- ❌ Integration: New features not accessible
- ❌ Database: Models created but tables don't exist
- ❌ Testing: Cannot test new endpoints

### After Completion:
- ✅ All new endpoints accessible
- ✅ Database operational with tables
- ✅ Monitoring and logging active
- ✅ Ready for JWT authentication
- ✅ Production readiness: 92%

---

## CRITICAL TASK #1: Integrate New Features into Main.py

**Priority**: 🔴 CRITICAL  
**Time**: 30 minutes  
**Impact**: Activates all 4 medium priority implementations  
**Dependencies**: None

### Why This is Critical:
- All new code (1,800+ lines) is currently isolated
- News API endpoints cannot be accessed
- Monitoring metrics not collected
- Logging middleware not active
- RBAC not enforced
- **BLOCKS**: Testing, production deployment, user access to new features

---

### Step 1: Check Current Router Structure

**File**: `src/api/v1/__init__.py`

```bash
# View current router structure
cat src/api/v1/__init__.py
```

**Expected Structure**:
```python
from fastapi import APIRouter
from src.api.v1 import health, ocr, ingest, feed

router = APIRouter()
router.include_router(health.router, tags=["Health"])
router.include_router(ocr.router, tags=["OCR"])
router.include_router(ingest.router, tags=["Ingestion"])
router.include_router(feed.router, tags=["Feed"])
```

---

### Step 2: Add News Router to V1 Router

**File**: `src/api/v1/__init__.py`

**Changes**:
1. Import news module
2. Include news router

```python
# Add import
from src.api.v1 import health, ocr, ingest, feed, news

# Add router
router.include_router(news.router, tags=["News"])
```

**Complete Updated File**:
```python
"""API v1 router aggregation."""
from fastapi import APIRouter
from src.api.v1 import health, ocr, ingest, feed, news

router = APIRouter()

# Include all v1 routers
router.include_router(health.router, tags=["Health"])
router.include_router(ocr.router, tags=["OCR"])
router.include_router(ingest.router, tags=["Ingestion"])
router.include_router(feed.router, tags=["Feed"])
router.include_router(news.router, tags=["News"])  # NEW
```

---

### Step 3: Update Main.py with Middleware and Logging

**File**: `src/main.py`

**Changes Required**:
1. Import new modules
2. Setup logging on startup
3. Add logging middleware
4. Add metrics middleware
5. Add metrics endpoint
6. Initialize database on startup

**Imports to Add** (after existing imports):
```python
from src.middleware.logging import LoggingMiddleware
from src.monitoring.metrics import metrics_middleware, get_metrics
from src.utils.logger import setup_logging
from src.database import init_db, check_db_connection
```

**Update Lifespan Function**:
```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan events."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Environment: {settings.environment}")
    print(f"Debug mode: {settings.debug}")
    
    # Setup structured logging
    setup_logging(level="INFO" if not settings.debug else "DEBUG")
    print("✓ Structured logging configured")
    
    # Initialize database (if configured)
    try:
        if hasattr(settings, 'database_url') and settings.database_url:
            await init_db()
            db_healthy = await check_db_connection()
            if db_healthy:
                print("✓ Database connection established")
            else:
                print("⚠ Database connection failed (optional for current features)")
        else:
            print("ℹ Database not configured (optional for current features)")
    except Exception as e:
        print(f"⚠ Database initialization failed: {e}")
        print("  Application will run without database features")
    
    yield
    
    # Shutdown
    print("Shutting down application")
```

**Add Middleware** (after existing middleware):
```python
# Add logging middleware (BEFORE other middleware for proper request tracking)
app.add_middleware(LoggingMiddleware)

# Add metrics middleware
app.middleware("http")(metrics_middleware)
```

**Add Metrics Endpoint** (after health_check function):
```python
@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Prometheus metrics endpoint."""
    return await get_metrics()
```

---

### Step 4: Complete Updated Main.py

**Full File**: `src/main.py`

```python
"""Main FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.api.v1 import router as v1_router
from src.middleware.logging import LoggingMiddleware
from src.monitoring.metrics import metrics_middleware, get_metrics
from src.utils.logger import setup_logging
from src.database import init_db, check_db_connection

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan events."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Environment: {settings.environment}")
    print(f"Debug mode: {settings.debug}")
    
    # Setup structured logging
    setup_logging(level="INFO" if not settings.debug else "DEBUG")
    print("✓ Structured logging configured")
    
    # Initialize database (if configured)
    try:
        if hasattr(settings, 'database_url') and settings.database_url:
            await init_db()
            db_healthy = await check_db_connection()
            if db_healthy:
                print("✓ Database connection established")
            else:
                print("⚠ Database connection failed (optional for current features)")
        else:
            print("ℹ Database not configured (optional for current features)")
    except Exception as e:
        print(f"⚠ Database initialization failed: {e}")
        print("  Application will run without database features")
    
    yield
    
    # Shutdown
    print("Shutting down application")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Lightweight API for newspaper ingestion with OCR, AI processing, and personalized news feeds",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)


# Middleware - ORDER MATTERS!
# 1. Logging middleware (first to capture all requests)
app.add_middleware(LoggingMiddleware)

# 2. CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. GZip middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 4. Metrics middleware
app.middleware("http")(metrics_middleware)


# Include API routers
app.include_router(v1_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "environment": settings.environment,
        "docs_url": "/docs" if settings.debug else None,
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "version": settings.app_version,
    }


@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Prometheus metrics endpoint."""
    return await get_metrics()


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__,
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
```

---

### Step 5: Verification Steps

**1. Check Application Starts**:
```bash
cd /Users/loan/Desktop/Mvuvi/vuva
source venv/bin/activate
python -m src.main
```

**Expected Output**:
```
Starting Vuva v1.2.0
Environment: development
Debug mode: True
✓ Structured logging configured
ℹ Database not configured (optional for current features)
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**2. Test New Endpoints**:
```bash
# View API documentation
open http://127.0.0.1:8000/docs

# Test news sources endpoint
curl http://127.0.0.1:8000/api/v1/news/sources

# Test metrics endpoint
curl http://127.0.0.1:8000/metrics
```

**3. Verify Logging**:
```bash
# Check logs directory created
ls -la logs/

# View structured logs
tail -f logs/app.log | jq
```

**4. Check Available Endpoints**:
```bash
curl http://127.0.0.1:8000/api/v1/news/ | jq
```

Expected new endpoints:
- `/api/v1/news/sources`
- `/api/v1/news/categories`
- `/api/v1/news/technology`
- `/api/v1/news/hackernews/top`
- `/api/v1/news/extract`
- `/metrics`

---

### Success Criteria:
- ✅ Application starts without errors
- ✅ `/metrics` endpoint returns Prometheus metrics
- ✅ News API endpoints return 200 OK (or appropriate responses)
- ✅ `logs/app.log` file created with JSON logs
- ✅ Request tracking headers present (X-Request-ID, X-Process-Time)
- ✅ OpenAPI docs show all new endpoints

---

## CRITICAL TASK #2: Setup Database and Run Migrations

**Priority**: 🔴 CRITICAL  
**Time**: 1 hour  
**Impact**: Enables data persistence, authentication, user management  
**Dependencies**: Task #1 completed

### Why This is Critical:
- Database tables don't exist yet
- Cannot store users, articles, API keys
- Cannot persist news sources or preferences
- **BLOCKS**: JWT authentication, user management, article storage
- Migration files ready but not executed

---

### Step 1: Install PostgreSQL

**macOS (Homebrew)**:
```bash
# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Verify installation
psql --version
```

**Expected Output**:
```
psql (PostgreSQL) 15.x
```

**Alternative: Use Docker**:
```bash
# Run PostgreSQL in Docker
docker run --name vuva-postgres \
  -e POSTGRES_PASSWORD=vuva_dev_password \
  -e POSTGRES_USER=vuva_user \
  -e POSTGRES_DB=vuva_db \
  -p 5432:5432 \
  -d postgres:15

# Verify container running
docker ps | grep vuva-postgres
```

---

### Step 2: Create Database

**Option A: Using psql CLI**:
```bash
# Connect to PostgreSQL
psql postgres

# Create database and user
CREATE USER vuva_user WITH PASSWORD 'vuva_dev_password';
CREATE DATABASE vuva_db OWNER vuva_user;
GRANT ALL PRIVILEGES ON DATABASE vuva_db TO vuva_user;

# Exit psql
\q
```

**Option B: Using createdb command**:
```bash
# Create database
createdb vuva_db

# Verify
psql -l | grep vuva_db
```

**Option C: Database Already Created (Docker)**:
If using Docker, database is automatically created.

---

### Step 3: Configure Environment Variables

**File**: `.env`

**Add Database Configuration**:
```bash
# Open .env file
nano .env
```

**Add these lines**:
```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://vuva_user:vuva_dev_password@localhost:5432/vuva_db
DATABASE_ECHO=False  # Set to True for SQL query logging

# Alternative for Docker
# DATABASE_URL=postgresql+asyncpg://vuva_user:vuva_dev_password@localhost:5432/vuva_db
```

**Full .env Example**:
```env
# Application Settings
APP_NAME=Vuva
APP_VERSION=1.2.0
ENVIRONMENT=development
DEBUG=True
HOST=127.0.0.1
PORT=8000

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Database Configuration
DATABASE_URL=postgresql+asyncpg://vuva_user:vuva_dev_password@localhost:5432/vuva_db
DATABASE_ECHO=False

# OCR Configuration
TESSERACT_PATH=/opt/homebrew/bin/tesseract

# Rate Limiting
RATE_LIMIT_ENABLED=True
```

---

### Step 4: Update Config to Load Database URL

**File**: `src/config.py`

**Add Database Settings**:
```python
# Find the Settings class and add:

class Settings(BaseSettings):
    # ... existing fields ...
    
    # Database
    database_url: str = ""
    database_echo: bool = False
    
    # ... rest of the class ...
```

**Complete Updated Settings Class**:
```python
class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "Vuva"
    app_version: str = "1.2.0"
    environment: str = "development"
    debug: bool = True
    host: str = "127.0.0.1"
    port: int = 8000
    
    # Security
    secret_key: str = "change-this-secret-key-in-production"
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Database
    database_url: str = ""
    database_echo: bool = False
    
    # OCR
    tesseract_path: str = "/usr/local/bin/tesseract"
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )
```

---

### Step 5: Update Alembic Configuration

**File**: `alembic.ini`

**Update sqlalchemy.url**:
```ini
# Find this line (around line 63):
sqlalchemy.url = driver://user:pass@localhost/dbname

# Replace with:
# sqlalchemy.url will be set dynamically from env.py
# Leave as placeholder or comment out
# sqlalchemy.url = 
```

**File**: `alembic/env.py`

**Verify Dynamic URL Configuration** (should already be present):
```python
# Around line 20-30, should have:
from src.config import get_settings
from src.models import Base

config.set_main_option("sqlalchemy.url", get_settings().database_url)
target_metadata = Base.metadata
```

---

### Step 6: Install Database Dependencies

```bash
cd /Users/loan/Desktop/Mvuvi/vuva
source venv/bin/activate

# Install database dependencies
pip install asyncpg psycopg2-binary

# Verify alembic installed
alembic --version
```

**Expected Output**:
```
alembic 1.16.5
```

---

### Step 7: Run Database Migrations

**Test Database Connection**:
```bash
# Verify database URL is correct
python -c "from src.config import get_settings; print(get_settings().database_url)"
```

**Expected Output**:
```
postgresql+asyncpg://vuva_user:vuva_dev_password@localhost:5432/vuva_db
```

**Run Migration**:
```bash
# Apply all migrations
alembic upgrade head
```

**Expected Output**:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Initial schema
```

**If Error Occurs**:
```bash
# Check database connection
psql -U vuva_user -d vuva_db -h localhost

# Check alembic history
alembic history

# Check current version
alembic current
```

---

### Step 8: Verify Database Tables Created

**Connect to Database**:
```bash
psql -U vuva_user -d vuva_db -h localhost
```

**Check Tables**:
```sql
-- List all tables
\dt

-- Expected output:
--  Schema |      Name        | Type  |   Owner
-- --------+------------------+-------+-----------
--  public | users            | table | vuva_user
--  public | sources          | table | vuva_user
--  public | articles         | table | vuva_user
--  public | api_keys         | table | vuva_user
--  public | user_preferences | table | vuva_user
--  public | audit_logs       | table | vuva_user
--  public | ocr_jobs         | table | vuva_user
--  public | alembic_version  | table | vuva_user

-- Check table structure
\d users

-- Exit
\q
```

**Alternative: Using SQL Query**:
```bash
psql -U vuva_user -d vuva_db -h localhost -c "\dt"
```

---

### Step 9: Create Initial Test Data (Optional)

**Create Test User Script**:
```bash
# Create test data script
cat > create_test_data.py << 'EOF'
import asyncio
from src.database import get_db_context
from src.models import User, Source
from sqlalchemy import select

async def create_test_data():
    async with get_db_context() as db:
        # Check if test user exists
        result = await db.execute(select(User).where(User.email == "test@vuva.com"))
        existing_user = result.scalar_one_or_none()
        
        if not existing_user:
            # Create test user
            test_user = User(
                email="test@vuva.com",
                password_hash="hashed_password_here",  # Will be replaced with JWT
                role="free",
                is_active=True,
                is_verified=True
            )
            db.add(test_user)
            print("✓ Created test user: test@vuva.com")
        else:
            print("ℹ Test user already exists")
        
        # Create test news source
        result = await db.execute(select(Source).where(Source.name == "TechCrunch"))
        existing_source = result.scalar_one_or_none()
        
        if not existing_source:
            tech_source = Source(
                name="TechCrunch",
                url="https://techcrunch.com/feed/",
                category="technology",
                feed_type="rss",
                is_active=True
            )
            db.add(tech_source)
            print("✓ Created test source: TechCrunch")
        else:
            print("ℹ Test source already exists")
        
        await db.commit()
        print("✅ Test data created successfully")

if __name__ == "__main__":
    asyncio.run(create_test_data())
EOF

# Run test data creation
python create_test_data.py
```

---

### Step 10: Verify Database Integration in Application

**Start Application**:
```bash
python -m src.main
```

**Expected Output**:
```
Starting Vuva v1.2.0
Environment: development
Debug mode: True
✓ Structured logging configured
✓ Database connection established
INFO:     Started server process
```

**Test Database-Dependent Endpoints**:
```bash
# Test endpoint that may use database (future)
curl http://127.0.0.1:8000/api/v1/news/sources
```

---

### Success Criteria:
- ✅ PostgreSQL installed and running
- ✅ Database `vuva_db` created
- ✅ DATABASE_URL configured in .env
- ✅ Migration executed successfully (`alembic upgrade head`)
- ✅ 7 tables + alembic_version table exist
- ✅ Application starts with "Database connection established"
- ✅ No database connection errors in logs
- ✅ Can query database tables

---

## Troubleshooting

### Issue: PostgreSQL Connection Failed

**Symptoms**:
```
asyncpg.exceptions.InvalidCatalogNameError: database "vuva_db" does not exist
```

**Solution**:
```bash
# Create database
createdb vuva_db

# Or via psql
psql postgres -c "CREATE DATABASE vuva_db;"
```

---

### Issue: Permission Denied

**Symptoms**:
```
FATAL: role "vuva_user" does not exist
```

**Solution**:
```bash
# Create user
psql postgres -c "CREATE USER vuva_user WITH PASSWORD 'vuva_dev_password';"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE vuva_db TO vuva_user;"
```

---

### Issue: Port Already in Use

**Symptoms**:
```
ERROR: [Errno 48] Address already in use
```

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port in .env
PORT=8001
```

---

### Issue: Migration Already Applied

**Symptoms**:
```
Target database is not up to date.
```

**Solution**:
```bash
# Check current version
alembic current

# Check available migrations
alembic history

# Force upgrade
alembic upgrade head

# Or downgrade and re-upgrade
alembic downgrade base
alembic upgrade head
```

---

### Issue: Missing Dependencies

**Symptoms**:
```
ModuleNotFoundError: No module named 'asyncpg'
```

**Solution**:
```bash
# Install missing dependencies
pip install asyncpg psycopg2-binary sqlalchemy alembic
```

---

## Post-Implementation Verification

### Final Checklist:

**Task #1 - Integration**:
- [ ] `src/api/v1/__init__.py` includes news router
- [ ] `src/main.py` imports new middleware
- [ ] LoggingMiddleware added
- [ ] Metrics middleware added
- [ ] `/metrics` endpoint exists
- [ ] Application starts successfully
- [ ] `/api/v1/news/*` endpoints accessible
- [ ] `logs/app.log` created
- [ ] Structured logs visible

**Task #2 - Database**:
- [ ] PostgreSQL installed
- [ ] Database `vuva_db` created
- [ ] `DATABASE_URL` in .env
- [ ] `alembic upgrade head` successful
- [ ] 8 tables exist (7 + alembic_version)
- [ ] Application connects to database
- [ ] No database errors in logs
- [ ] Can query tables via psql

---

## Next Steps After Completion

### Immediate (Same Day):
1. **Run Test Suite**:
   ```bash
   pytest tests/ -v --cov=src
   ```

2. **Fix Failing Tests**:
   - Align news ingestion tests with implementation
   - Add database tests
   - Achieve >80% coverage

### Short-term (Next Day):
3. **Implement JWT Authentication**:
   - Create auth endpoints
   - Add password hashing
   - Generate JWT tokens
   - Protect endpoints

4. **Setup CI/CD**:
   - Create GitHub Actions workflow
   - Automated testing
   - Code coverage reporting
   - Deployment pipeline

---

## Production Readiness Tracking

### Before Critical Tasks:
- Overall: 85%
- Backend: 90%
- Integration: 60%
- Database: 70%
- Testing: 65%

### After Critical Tasks:
- Overall: 92%
- Backend: 95%
- Integration: 95%
- Database: 90%
- Testing: 70%

### After JWT + Tests:
- Overall: 96%
- Backend: 98%
- Integration: 98%
- Database: 95%
- Testing: 90%

---

## Resources

### Documentation:
- [PRIORITY_TASKS.md](./PRIORITY_TASKS.md) - Full priority task list
- [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) - Medium priority implementation details
- [FastAPI Docs](https://fastapi.tiangolo.com/) - Framework documentation
- [Alembic Docs](https://alembic.sqlalchemy.org/) - Migration tool
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/) - ORM documentation

### Code References:
- Database Models: `src/models/__init__.py`
- News API: `src/api/v1/news.py`
- RBAC: `src/middleware/authorization.py`
- Monitoring: `src/monitoring/metrics.py`
- Logging: `src/utils/logger.py`

---

**Last Updated**: January 24, 2026  
**Version**: 1.0  
**Status**: Ready for Implementation  
**Estimated Completion**: 1.5 hours
