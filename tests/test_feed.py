"""Tests for news feed endpoints."""


import pytest

@pytest.mark.asyncio
async def test_feed_endpoint(client):
    """Test news feed endpoint."""
    response = await client.get("/api/v1/feed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "pagination" in data


@pytest.mark.asyncio
async def test_feed_with_filters(client):
    """Test feed with category filter."""
    response = await client.get("/api/v1/feed?category=technology&page_size=10")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_article(client):
    """Test get specific article."""
    response = await client.get("/api/v1/feed/article/test-article-123")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


@pytest.mark.asyncio
async def test_news_sources(client):
    """Test get news sources."""
    response = await client.get("/api/v1/feed/sources")
    assert response.status_code == 200
    data = response.json()
    assert "sources" in data["data"]


@pytest.mark.asyncio
async def test_update_preferences(client):
    """Test update feed preferences."""
    response = await client.post(
        "/api/v1/feed/preferences",
        params={
            "categories": ["technology", "science"],
            "languages": ["en"],
        },
    )
    assert response.status_code == 200
