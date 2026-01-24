# Testing Documentation

> Comprehensive testing strategy and guidelines for Vuva API

**Last Updated:** January 24, 2026  
**Test Coverage Target:** 80%+  
**Current Coverage:** ~75% (estimated)

---

## Overview

Vuva employs a comprehensive testing strategy covering unit tests, integration tests, security tests, and performance benchmarks. All tests are written with pytest and follow industry best practices.

---

## Test Suites

### 1. OCR Test Suite (`tests/test_ocr.py`)

**Lines:** 650+  
**Test Classes:** 14  
**Test Cases:** 25+  
**Coverage:** OCR engine integration, preprocessing, batch processing

#### Test Classes

1. **TestImagePreprocessing** - Image manipulation and enhancement
2. **TestTesseractOCR** - Tesseract engine functionality
3. **TestEasyOCR** - EasyOCR engine functionality
4. **TestPaddleOCR** - PaddleOCR engine functionality
5. **TestOCRComparison** - Multi-engine comparison
6. **TestBatchProcessing** - Batch OCR operations
7. **TestOCREndpoints** - API endpoint validation
8. **TestErrorHandling** - Error scenarios and edge cases
9. **TestFileValidation** - File type and content validation
10. **TestSecurityFeatures** - Path traversal, injection protection
11. **TestPerformanceBenchmarks** - Speed and efficiency tests
12. **TestQualityValidation** - Confidence scoring
13. **TestMultiLanguageSupport** - Language detection
14. **TestIntegration** - End-to-end workflows

#### Key Features Tested

- ✅ Image preprocessing (grayscale, denoise, threshold)
- ✅ OCR engine lazy loading
- ✅ Multi-engine comparison
- ✅ Batch processing with concurrency
- ✅ Error handling and recovery
- ✅ File format validation
- ✅ Security protection (path traversal, injection)
- ✅ Performance benchmarks (speed requirements)
- ✅ Quality validation (confidence thresholds)

#### Running OCR Tests

```bash
# Run all OCR tests
pytest tests/test_ocr.py -v

# Run specific test class
pytest tests/test_ocr.py::TestTesseractOCR -v

# Run with coverage
pytest tests/test_ocr.py --cov=src/services/ocr_service --cov-report=html

# Run performance benchmarks only
pytest tests/test_ocr.py::TestPerformanceBenchmarks -v
```

---

### 2. Authentication Test Suite (`tests/test_authentication.py`)

**Lines:** 550+  
**Test Classes:** 8  
**Test Cases:** 30+  
**Coverage:** Authentication, JWT, API keys, security

#### Test Classes

1. **TestPasswordHashing** - Argon2id password hashing
2. **TestUserRegistration** - User registration flow
3. **TestLogin** - Login and token generation
4. **TestTokens** - JWT token structure and validation
5. **TestTokenRefresh** - Refresh token mechanism
6. **TestProtectedEndpoints** - Authorization middleware
7. **TestPasswordChange** - Password update flow
8. **TestAPIKeys** - API key management
9. **TestSecurityFeatures** - Security validation

#### Key Features Tested

- ✅ Argon2id password hashing (64MB memory, 3 iterations)
- ✅ Password verification with timing-attack resistance
- ✅ Different passwords produce different hashes (salt)
- ✅ User registration with email/password validation
- ✅ Duplicate email detection
- ✅ Weak password rejection (length, uppercase, digit)
- ✅ Invalid email rejection
- ✅ Login with JWT token generation
- ✅ Wrong password handling
- ✅ Non-existent user handling
- ✅ JWT token structure (3 parts)
- ✅ Token decode and payload validation
- ✅ Expired token handling
- ✅ Invalid token handling
- ✅ Token refresh mechanism
- ✅ Access token rejection in refresh endpoint
- ✅ Protected endpoint access without token
- ✅ Protected endpoint access with valid token
- ✅ Protected endpoint access with invalid token
- ✅ Password change with current password verification
- ✅ Wrong current password rejection
- ✅ API key generation (vuva_ prefix)
- ✅ API key creation endpoint
- ✅ SQL injection protection
- ✅ Timing attack resistance on login
- ✅ Password rehashing detection

#### Running Authentication Tests

```bash
# Run all authentication tests
pytest tests/test_authentication.py -v

# Run specific test class
pytest tests/test_authentication.py::TestPasswordHashing -v

# Run with coverage
pytest tests/test_authentication.py --cov=src/services/auth_service --cov-report=html

# Run security tests only
pytest tests/test_authentication.py::TestSecurityFeatures -v

# Run with asyncio mode (for async tests)
pytest tests/test_authentication.py -v --asyncio-mode=auto
```

---

### 3. API Tests (`tests/test_api.py`)

**Status:** Existing  
**Coverage:** Basic health checks, feed endpoints

#### Running API Tests

```bash
# Run all API tests
pytest tests/test_api.py -v
```

---

### 4. Integration Tests (Planned)

**Status:** In Progress  
**Target:** Week 5

#### Planned Test Cases

- Database connection and transaction tests
- End-to-end authentication flow
- News ingestion pipeline
- OCR processing pipeline
- API endpoint integration
- Caching layer validation

---

## Test Database Setup

### In-Memory SQLite for Tests

Tests use an in-memory SQLite database for speed and isolation:

```python
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
```

### PostgreSQL Test Database (Optional)

For integration tests with PostgreSQL:

```bash
# Create test database
createdb vuva_test -U postgres

# Set test environment variable
export TEST_DATABASE_URL="postgresql+asyncpg://postgres:password@localhost/vuva_test"

# Run tests with PostgreSQL
pytest tests/test_integration.py -v
```

---

## Testing Best Practices

### 1. Test Structure

- **Arrange:** Set up test data and dependencies
- **Act:** Execute the function/endpoint being tested
- **Assert:** Verify the expected outcome

### 2. Test Isolation

- Each test should be independent
- Use fixtures for setup/teardown
- Reset database state between tests
- Mock external dependencies

### 3. Test Coverage

- Aim for 80%+ code coverage
- Focus on critical paths first
- Test edge cases and error scenarios
- Include security validation tests

### 4. Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`
- Descriptive names: `test_register_with_weak_password`

### 5. Async Testing

- Use `@pytest.mark.asyncio` decorator
- Use `pytest-asyncio` plugin
- Configure asyncio mode in `pytest.ini`

---

## Running All Tests

### Run All Tests

```bash
# Run all tests with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_authentication.py -v

# Run specific test class
pytest tests/test_authentication.py::TestPasswordHashing -v

# Run specific test function
pytest tests/test_authentication.py::TestPasswordHashing::test_password_hashing -v
```

### Generate Coverage Report

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html

# Open coverage report in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Run Tests in Parallel

```bash
# Install pytest-xdist
pip install pytest-xdist

# Run tests in parallel (4 workers)
pytest -n 4 -v
```

---

## Test Configuration

### pytest.ini

```ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
markers =
    asyncio: marks tests as async
    slow: marks tests as slow
    integration: marks tests as integration tests
```

### conftest.py

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Global test fixtures
@pytest.fixture
async def db_session():
    """Create test database session."""
    # Setup
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
    
    # Teardown
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
def client():
    """Create test FastAPI client."""
    return TestClient(app)
```

---

## Security Testing

### Password Hashing Tests

- ✅ Argon2id algorithm verification
- ✅ Hash uniqueness (salt verification)
- ✅ Correct password verification
- ✅ Incorrect password rejection
- ✅ Timing attack resistance

### Authentication Tests

- ✅ SQL injection protection
- ✅ Token validation
- ✅ Expired token handling
- ✅ Invalid token handling
- ✅ Authorization middleware

### Input Validation Tests

- ✅ Email format validation
- ✅ Password strength requirements
- ✅ Path traversal protection
- ✅ File content validation

---

## Performance Benchmarks

### OCR Performance Tests

```python
def test_fast_transcription_speed(self):
    """Test fast transcription meets speed requirement."""
    start = time.time()
    result = ocr_service.transcribe_fast(image)
    duration = time.time() - start
    assert duration < 0.5  # 500ms threshold
```

### Timing Attack Tests

```python
def test_timing_attack_resistance(self):
    """Test constant-time password verification."""
    time_correct = measure_verification_time(correct_password)
    time_incorrect = measure_verification_time(wrong_password)
    time_diff = abs(time_correct - time_incorrect)
    assert time_diff < 0.05  # 50ms threshold
```

---

## Test Metrics

### Current Status

| Test Suite | Test Cases | Coverage | Status |
|------------|-----------|----------|--------|
| OCR Tests | 25+ | ~80% | ✅ Complete |
| Auth Tests | 30+ | ~85% | ✅ Complete |
| API Tests | 10+ | ~60% | ✅ Existing |
| Integration | 0 | 0% | 🔄 Planned |
| **Total** | **65+** | **~75%** | **In Progress** |

### Target Metrics

- **Overall Coverage:** 80%+
- **Critical Path Coverage:** 95%+
- **Security Test Coverage:** 100%
- **Performance Tests:** 100%

---

## Continuous Integration (Planned)

### GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v2
        with:
          file: ./coverage.xml
```

---

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure `PYTHONPATH` includes project root
   - Run tests from project root: `pytest tests/`

2. **Async Test Failures**
   - Check `pytest-asyncio` is installed
   - Verify `asyncio_mode = auto` in `pytest.ini`

3. **Database Connection Errors**
   - Ensure test database URL is correct
   - Check PostgreSQL is running for integration tests

4. **Timing Tests Failing**
   - System load can affect timing tests
   - Increase tolerance thresholds if needed
   - Run timing tests in isolation

---

## Test Dependencies

### Required Packages

```bash
pytest==8.4.2
pytest-asyncio==0.23.0
pytest-cov==4.1.0
pytest-xdist==3.5.0  # Optional: parallel testing
httpx==0.25.0  # For async client testing
```

### Installation

```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

---

## Contributing Tests

### Writing New Tests

1. Create test file in `tests/` directory
2. Follow naming conventions
3. Write descriptive test names
4. Include docstrings
5. Test both success and failure paths
6. Add edge case tests
7. Include security validation

### Test Review Checklist

- [ ] Test file follows naming convention
- [ ] Tests are independent and isolated
- [ ] Tests have clear assertions
- [ ] Edge cases are covered
- [ ] Error scenarios are tested
- [ ] Security validation included
- [ ] Performance benchmarks added (if applicable)
- [ ] Documentation updated

---

## Future Testing Plans

### Phase 3: Intelligence Testing (Week 5-6)

- Neural network model tests
- Randomization algorithm tests
- Agentic system tests
- NLP pipeline tests

### Phase 4: Frontend Testing (Week 7-8)

- React component tests (Jest)
- E2E tests (Playwright/Cypress)
- WebSocket connection tests
- UI/UX validation tests

### Phase 5: Production Testing (Week 9-10)

- Load testing (Locust)
- Stress testing
- Security penetration testing
- Performance profiling

---

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing Guide](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)

---

**For questions or issues with testing, please refer to the project documentation or create an issue on GitHub.**
