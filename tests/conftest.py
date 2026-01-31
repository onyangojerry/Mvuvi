"""Test configuration and fixtures.

Simplified test setup using httpx AsyncClient with proper async context.
This approach ensures FastAPI's dependency injection works correctly with async database sessions.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool

from src.main import app
from src.config import Settings, get_settings
from src.database import Base, get_db



# --- Parallel test DB isolation ---
import random, string
import contextvars

_db_suffix = contextvars.ContextVar("db_suffix", default=None)

def _random_suffix():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def get_test_db_url():
    suffix = _db_suffix.get()
    if not suffix:
        suffix = _random_suffix()
        _db_suffix.set(suffix)
    return f"sqlite+aiosqlite:///file:memdb_{suffix}?mode=memory&cache=shared"

def get_test_settings():
    """Get test settings override with unique DB per test."""
    return Settings(
        environment="testing",
        debug=True,
        database_url=get_test_db_url(),
        redis_url="redis://localhost:6379/1",
        cache_enabled=True,
        secret_key="test-secret-key-for-jwt-tokens-in-testing-environment-only",
    )

def create_test_engine():
    return create_async_engine(
        get_test_db_url(),
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

def create_test_session_local(engine):
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

test_engine = create_test_engine()
TestSessionLocal = create_test_session_local(test_engine)


async def override_get_db():
    """Override database dependency with test database session.
    
    This is a generator function that yields a database session.
    FastAPI's dependency injection will handle calling this generator.
    """
    session = TestSessionLocal()
    try:
        yield session
    finally:
        await session.close()


@pytest.fixture(scope="function")
def anyio_backend():
    """Use asyncio backend for anyio."""
    return "asyncio"


@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_test_db():
    """Set up and tear down test database for each test (parallel safe)."""
    # Assign a new DB suffix for this test context
    import random, string
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    _db_suffix.set(suffix)
    global test_engine, TestSessionLocal
    test_engine = create_test_engine()
    TestSessionLocal = create_test_session_local(test_engine)
    # Create all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Drop all tables after test
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client():
    """Create async HTTP client for testing.
    
    This fixture:
    - Overrides app settings to use test configuration
    - Overrides database dependency to use test database
    - Creates an async HTTP client using httpx
    - Cleans up dependencies after test
    """
    # Override dependencies
    app.dependency_overrides[get_settings] = get_test_settings
    app.dependency_overrides[get_db] = override_get_db
    
    # Create async client
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
        follow_redirects=True,
    ) as ac:
        yield ac
    
    # Clean up
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def authenticated_client(client):
    """Create an authenticated client with a registered user and token.
    
    Returns:
        tuple: (client, token, user_data)
    """
    # Register a test user
    user_data = {
        "email": "testuser@example.com",
        "password": "TestPass123"
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    
    # Login to get token
    response = await client.post("/api/v1/auth/login", json=user_data)
    assert response.status_code == 200
    token_data = response.json()
    
    return client, token_data["access_token"], user_data


@pytest_asyncio.fixture(scope="function")
async def test_db_session():
    """Get a database session for direct database operations in tests.
    
    Use this fixture when you need to directly access the database in tests.
    """
    session = TestSessionLocal()
    try:
        yield session
    finally:
        await session.close()
