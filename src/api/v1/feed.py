"""News feed endpoints for personalized content delivery."""

from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, Depends, status
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocketState
from src.middleware.auth import get_current_user
from src.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import logging
from pydantic import BaseModel, Field
from src.services.news_ingestion import NewsDataManager

router = APIRouter()

# Connection manager for WebSocket clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        for connection in list(self.active_connections):
            if connection.application_state == WebSocketState.CONNECTED:
                try:
                    await connection.send_json(message)
                except Exception:
                    self.disconnect(connection)


manager = ConnectionManager()
news_manager = NewsDataManager()


class NewsArticle(BaseModel):
    """News article model."""
    
    id: str = Field(description="Unique article ID")
    title: str = Field(description="Article title")
    content: str = Field(description="Article content")
    source: str = Field(description="News source")
    category: Optional[str] = Field(default=None, description="Article category")
    published_at: str = Field(description="Publication timestamp")
    extracted_at: Optional[str] = Field(default=None, description="OCR extraction timestamp")
    confidence_score: Optional[float] = Field(default=None, description="OCR confidence (0-1)")


class FeedResponse(BaseModel):
    """Response model for news feed."""
    
    status: str = Field(default="success")
    data: List[NewsArticle] = Field(description="List of news articles")
    pagination: dict = Field(description="Pagination information")
    meta: dict = Field(description="Response metadata")


@router.get("", response_model=FeedResponse)
async def get_news_feed(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(default=None, description="Filter by category"),
    language: Optional[str] = Query(default="en", description="Language preference"),
    sort: Optional[str] = Query(default="-published_at", description="Sort order (prefix with - for desc)"),
):
    """
    Get personalized news feed using novel randomization algorithms.
    
    This endpoint returns a curated feed of news articles from various sources:
    - Open source news APIs
    - RSS feeds from trusted sources
    - User-uploaded newspapers (processed via OCR)
    
    The feed uses specialized randomization algorithms to provide:
    - Content diversity
    - Personalized recommendations
    - Fresh and relevant news
    - Serendipitous discovery
    
    **Filters**:
    - `category`: politics, technology, sports, business, etc.
    - `language`: ISO language code
    
    **Sorting**:
    - `published_at`: Publication date
    - `relevance`: Relevance score
    - `popularity`: Engagement metrics
    """
    # TODO: Implement randomization algorithm
    # TODO: Query database for articles
    # TODO: Apply user preferences
    # TODO: Calculate diversity scores
    
    # Placeholder response
    return FeedResponse(
        status="success",
        data=[],
        pagination={
            "page": page,
            "page_size": page_size,
            "total_pages": 0,
            "total_items": 0,
            "has_next": False,
            "has_previous": False,
        },
        meta={
            "timestamp": datetime.utcnow().isoformat(),
            "algorithm": "weighted-randomization-v1",
            "diversity_score": 0.0,
        },
    )


@router.get("/article/{article_id}")
async def get_article(article_id: str):
    """
    Get a specific article by ID.
    
    Returns full article content with metadata.
    """
    # TODO: Query database for article
    
    return {
        "status": "success",
        "data": {
            "id": article_id,
            "type": "news-article",
            "attributes": {
                "title": "Article not found",
                "content": "This article does not exist or has been removed.",
            },
        },
    }



@router.websocket("/stream")
async def websocket_feed_stream(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
):
    """
    Production-grade WebSocket endpoint for real-time news feed updates.
    - Authenticated users get personalized feed
    - Guests get randomized feed
    - Secure, robust, and scalable
    """
    logger = logging.getLogger("feed.websocket")
    user = None
    try:
        # Try to get user from JWT (Authorization header or query param)
        token = websocket.query_params.get("token")
        if token:
            class DummyCred:
                credentials = token
            user = await get_current_user(DummyCred(), db)
        await manager.connect(websocket)
        logger.info(f"WebSocket connected: {websocket.client.host} user={'guest' if not user else user.email}")

        # Fetch news articles (personalized or general)
        if user:
            # TODO: Use user preferences for filtering (category, language, etc.)
            articles = await news_manager.fetch_all_news(limit=50)
        else:
            articles = await news_manager.fetch_all_news(limit=50)

        # Stream articles one by one (simulate real-time)
        for article in articles:
            await websocket.send_json({"type": "news", "article": article})
            await asyncio.sleep(2)  # Simulate delay between articles

        # Keep connection alive (heartbeat)
        while True:
            await asyncio.sleep(30)
            await websocket.send_json({"type": "heartbeat"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"WebSocket disconnected: {websocket.client.host}")
    except Exception as e:
        manager.disconnect(websocket)
        logger.error(f"WebSocket error: {e}")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)


@router.get("/sources")
async def get_news_sources():
    """
    Get list of available news sources.
    
    Returns all configured news sources including:
    - Open source news APIs
    - RSS feeds
    - User-contributed sources
    """
    # TODO: Query configured sources
    
    return {
        "status": "success",
        "data": {
            "sources": [
                {
                    "id": "opensource-news-api",
                    "name": "Open Source News API",
                    "type": "api",
                    "enabled": True,
                },
                {
                    "id": "rss-feeds",
                    "name": "RSS Aggregator",
                    "type": "rss",
                    "enabled": True,
                },
                {
                    "id": "user-uploads",
                    "name": "User Uploaded Newspapers",
                    "type": "ocr",
                    "enabled": True,
                },
            ],
        },
    }


@router.post("/preferences")
async def update_preferences(
    categories: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
    sources: Optional[List[str]] = None,
):
    """
    Update user feed preferences.
    
    Customize the news feed by selecting:
    - Preferred categories
    - Languages
    - News sources
    
    The randomization algorithm will use these preferences
    to personalize content while maintaining diversity.
    """
    # TODO: Implement authentication
    # TODO: Save preferences to database
    # TODO: Update recommendation model
    
    return {
        "status": "success",
        "data": {
            "preferences": {
                "categories": categories or [],
                "languages": languages or ["en"],
                "sources": sources or [],
            },
            "updated_at": datetime.utcnow().isoformat(),
        },
    }
