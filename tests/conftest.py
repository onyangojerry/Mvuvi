"""Test configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.config import Settings, get_settings


def get_test_settings():
    """Override settings for testing."""
    return Settings(
        environment="testing",
        debug=True,
        database_url="sqlite+aiosqlite:///:memory:",
        redis_url="redis://localhost:6379/1",
    )


@pytest.fixture
def test_app():
    """Create test app with overridden settings."""
    app.dependency_overrides[get_settings] = get_test_settings
    yield app
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_app):
    """Create test client."""
    return TestClient(test_app)
