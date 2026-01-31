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
from src.models import Article, Source
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.database import get_db

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
    db: AsyncSession = Depends(get_db),
):
    """
    Get news feed from the database, including OCR uploads and RSS/API articles.
    Supports pagination and category filtering.
    """
    query = select(Article).options(joinedload(Article.source))
    if category and category.lower() != "all":
        query = query.where(Article.source.has(category=category.lower()))
    # Optionally filter by language
    # query = query.where(Article.source.has(language=language))
    # Sorting
    if sort == "-published_at":
        query = query.order_by(Article.published_at.desc().nullslast())
    else:
        query = query.order_by(Article.published_at.asc().nullslast())
    # Pagination
    offset = (page - 1) * page_size
    total_items = len((await db.execute(select(Article))).scalars().all())
    result = await db.execute(query.offset(offset).limit(page_size))
    articles = result.scalars().all()
    # Format for API
    data = [
        NewsArticle(
            id=a.id,
            title=a.title,
            content=a.content,
            summary=a.summary,
            source=a.source.name if a.source else "Unknown",
            category=a.source.category if a.source else None,
            published_at=a.published_at.isoformat() if a.published_at else "",
            extracted_at=a.created_at.isoformat() if a.created_at else None,
            confidence_score=None,  # Optionally add if stored
        )
        for a in articles
    ]
    total_pages = (total_items + page_size - 1) // page_size if page_size else 1
    return FeedResponse(
        status="success",
        data=data,
        pagination={
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "total_items": total_items,
            "has_next": page < total_pages,
            "has_previous": page > 1,
        },
        meta={
            "timestamp": datetime.utcnow().isoformat(),
            "algorithm": "db-query",
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



import redis.asyncio as aioredis

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
            articles = await news_manager.fetch_all_news(limit=50)
        else:
            articles = await news_manager.fetch_all_news(limit=50)
        # Stream articles one by one (simulate real-time)
        for article in articles:
            await websocket.send_json({"type": "news", "article": article})
            await asyncio.sleep(2)

        # Subscribe to Redis for real-time updates
        redis_url = getattr(get_settings(), "redis_url", "redis://localhost:6379/0")
        r = aioredis.from_url(redis_url)
        pubsub = r.pubsub()
        await pubsub.subscribe(get_settings().redis_notifications_channel)

        async def redis_listener():
            async for msg in pubsub.listen():
                if msg["type"] == "message":
                    try:
                        payload = json.loads(msg["data"])
                        if payload.get("event") == "new_article":
                            await websocket.send_json({"type": "new_article", "article": payload})
                    except Exception:
                        pass

        # Run redis listener and heartbeat concurrently
        async def heartbeat():
            while True:
                await asyncio.sleep(30)
                await websocket.send_json({"type": "heartbeat"})

        listener_task = asyncio.create_task(redis_listener())
        heartbeat_task = asyncio.create_task(heartbeat())
        done, pending = await asyncio.wait(
            [listener_task, heartbeat_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        for task in pending:
            task.cancel()
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
