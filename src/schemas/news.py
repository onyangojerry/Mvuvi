"""Pydantic schemas for news API."""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field


class NewsSourceResponse(BaseModel):
    """News source information."""
    name: str
    url: str
    category: str
    type: str  # rss, api, scrape
    is_active: bool


class CategoryResponse(BaseModel):
    """News category information."""
    name: str
    description: str
    source_count: int


class ArticleSummary(BaseModel):
    """Brief article information."""
    title: str
    url: HttpUrl
    summary: Optional[str] = None
    published: Optional[datetime] = None
    source: str
    author: Optional[str] = None


class ArticleListResponse(BaseModel):
    """Paginated list of articles."""
    articles: List[dict]
    total: int
    page: int
    pages: int
    category: str


class ArticleDetailResponse(BaseModel):
    """Full article content."""
    title: str
    text: str
    url: HttpUrl
    author: Optional[str] = None
    published: Optional[datetime] = None
    keywords: Optional[List[str]] = None
    summary: Optional[str] = None


class ArticleExtractionRequest(BaseModel):
    """Request to extract article content."""
    url: HttpUrl = Field(..., description="URL of the article to extract")


class HackerNewsResponse(BaseModel):
    """Hacker News story."""
    id: int
    title: str
    url: Optional[HttpUrl] = None
    score: int
    author: str
    time: datetime
    comments_count: int


class NewsSearchRequest(BaseModel):
    """Search request."""
    query: str = Field(..., min_length=2, max_length=200)
    categories: Optional[List[str]] = None
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)


class NewsSearchResponse(BaseModel):
    """Search results."""
    articles: List[ArticleSummary]
    total: int
    query: str
