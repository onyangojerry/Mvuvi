"""Tests for news feed endpoints."""


def test_feed_endpoint(client):
    """Test news feed endpoint."""
    response = client.get("/api/v1/feed")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert "pagination" in data


def test_feed_with_filters(client):
    """Test feed with category filter."""
    response = client.get("/api/v1/feed?category=technology&page_size=10")
    assert response.status_code == 200


def test_get_article(client):
    """Test get specific article."""
    response = client.get("/api/v1/feed/article/test-article-123")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


def test_news_sources(client):
    """Test get news sources."""
    response = client.get("/api/v1/feed/sources")
    assert response.status_code == 200
    data = response.json()
    assert "sources" in data["data"]


def test_update_preferences(client):
    """Test update feed preferences."""
    response = client.post(
        "/api/v1/feed/preferences",
        params={
            "categories": ["technology", "science"],
            "languages": ["en"],
        },
    )
    assert response.status_code == 200
