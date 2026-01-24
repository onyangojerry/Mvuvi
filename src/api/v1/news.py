"""
News API endpoints for Vuva.
Provides access to news from RSS feeds, Hacker News, and article extraction.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.schemas.news import (
    NewsSourceResponse,
    CategoryResponse,
    ArticleListResponse,
    ArticleDetailResponse,
    ArticleExtractionRequest,
    HackerNewsResponse,
    NewsSearchRequest,
    NewsSearchResponse
)
from src.services.news_ingestion import NewsDataManager
from src.middleware.authorization import require_permission
from src.monitoring.metrics import track_api_call

router = APIRouter(tags=["news"])
news_manager = NewsDataManager()


@router.get("/sources", response_model=List[NewsSourceResponse])
@track_api_call("news_sources_list")
async def list_news_sources(
    category: Optional[str] = Query(None, description="Filter by category"),
    active_only: bool = Query(True, description="Only active sources"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all available news sources.
    
    **Categories**: technology, world, business, science, general
    """
    sources = []
    
    # Get sources from news manager
    feed_sources = news_manager.rss_aggregator.feeds
    
    for cat, urls in feed_sources.items():
        if category and cat != category:
            continue
            
        for feed_url in urls:
            sources.append({
                "name": feed_url.split("/")[2],  # Extract domain
                "url": feed_url,
                "category": cat,
                "type": "rss",
                "is_active": active_only
            })
    
    # Add Hacker News
    if not category or category == "technology":
        sources.append({
            "name": "Hacker News",
            "url": "https://hacker-news.firebaseio.com/v0",
            "category": "technology",
            "type": "api",
            "is_active": True
        })
    
    return sources


@router.get("/categories", response_model=List[CategoryResponse])
@track_api_call("news_categories_list")
async def list_categories():
    """List all available news categories."""
    categories = [
        {"name": "technology", "description": "Tech news and updates", "source_count": 4},
        {"name": "world", "description": "World news and events", "source_count": 4},
        {"name": "business", "description": "Business and finance", "source_count": 3},
        {"name": "science", "description": "Scientific discoveries", "source_count": 3},
        {"name": "general", "description": "General news", "source_count": 4},
    ]
    return categories


@router.get("/{category}", response_model=ArticleListResponse)
@track_api_call("news_by_category")
@require_permission("read:news")
async def get_news_by_category(
    category: str,
    limit: int = Query(20, ge=1, le=100, description="Number of articles to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get news articles by category.
    
    **Categories**: technology, world, business, science, general
    
    **Pagination**: Use limit and offset for pagination.
    """
    valid_categories = ["technology", "world", "business", "science", "general"]
    
    if category not in valid_categories:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category. Must be one of: {', '.join(valid_categories)}"
        )
    
    try:
        # Fetch from RSS feeds
        articles = await news_manager.fetch_from_feeds([category], limit=limit+offset)
        
        # Apply pagination
        paginated_articles = articles[offset:offset+limit]
        
        return {
            "articles": paginated_articles,
            "total": len(articles),
            "page": offset // limit + 1,
            "pages": (len(articles) + limit - 1) // limit,
            "category": category
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch news: {str(e)}"
        )


@router.get("/hackernews/top", response_model=List[HackerNewsResponse])
@track_api_call("hackernews_top")
@require_permission("read:news")
async def get_hacker_news_top(
    limit: int = Query(10, ge=1, le=50, description="Number of stories to return")
):
    """
    Get top stories from Hacker News.
    
    **Rate Limit**: Respects Hacker News API limits.
    """
    try:
        stories = news_manager.hn_client.get_top_stories(limit=limit)
        return stories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch Hacker News: {str(e)}"
        )


@router.post("/extract", response_model=ArticleDetailResponse)
@track_api_call("article_extract")
@require_permission("read:full_articles")
async def extract_full_article(
    request: ArticleExtractionRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Extract full article content from a URL.
    
    **Requires**: Basic tier or higher.
    
    **Supports**: Most news websites and blogs.
    """
    try:
        article = news_manager.article_extractor.extract(request.url)
        
        if not article:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Failed to extract article content"
            )
        
        return article
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Extraction failed: {str(e)}"
        )


@router.post("/search", response_model=NewsSearchResponse)
@track_api_call("news_search")
@require_permission("read:news")
async def search_news(
    request: NewsSearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Search news articles by keyword.
    
    **Note**: Currently searches across all categories.
    Future versions will support category filtering.
    """
    # This would integrate with a full-text search engine
    # For now, return a placeholder
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Search functionality coming soon"
    )


@router.get("/all", response_model=dict)
@track_api_call("news_all")
@require_permission("read:news")
async def get_all_news(
    limit_per_category: int = Query(5, ge=1, le=20, description="Articles per category"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get news from all categories.
    
    **Response**: Dictionary with category names as keys and article lists as values.
    """
    try:
        all_news = await news_manager.fetch_from_feeds(
            categories=["technology", "world", "business", "science", "general"],
            limit=limit_per_category
        )
        return all_news
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch news: {str(e)}"
        )
