"""Free newspaper and news data ingestion services."""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

import feedparser
import requests
from newspaper import Article
from dateutil import parser as date_parser

logger = logging.getLogger(__name__)


class RSSFeedAggregator:
    """
    Aggregator for RSS feeds from various free news sources.
    
    Fetches and parses RSS feeds without requiring API keys.
    """
    
    # Comprehensive list of free news RSS feeds
    DEFAULT_FEEDS = {
        "technology": [
            "https://www.theverge.com/rss/index.xml",
            "https://techcrunch.com/feed/",
            "https://www.wired.com/feed/rss",
            "https://news.ycombinator.com/rss",
        ],
        "world": [
            "http://feeds.bbci.co.uk/news/world/rss.xml",
            "https://www.theguardian.com/world/rss",
            "https://www.aljazeera.com/xml/rss/all.xml",
            "https://rss.dw.com/xml/rss-en-all",
        ],
        "business": [
            "https://feeds.bloomberg.com/markets/news.rss",
            "https://www.ft.com/?format=rss",
            "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        ],
        "science": [
            "https://www.sciencedaily.com/rss/all.xml",
            "https://phys.org/rss-feed/",
            "https://www.nature.com/nature.rss",
        ],
        "general": [
            "http://feeds.bbci.co.uk/news/rss.xml",
            "http://rss.cnn.com/rss/edition.rss",
            "https://www.theguardian.com/uk/rss",
            "https://www.reddit.com/r/news/.rss",
        ],
    }
    
    def __init__(self):
        self.feeds = {}
        for category, urls in self.DEFAULT_FEEDS.items():
            self.feeds[category] = urls
        self.executor = ThreadPoolExecutor(max_workers=5)
    
    def _parse_feed(self, feed_url: str) -> List[Dict[str, Any]]:
        """Parse a single RSS feed synchronously."""
        try:
            logger.info(f"Fetching RSS feed: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            articles = []
            for entry in feed.entries:
                try:
                    # Extract published date
                    published = None
                    if hasattr(entry, 'published'):
                        published = date_parser.parse(entry.published)
                    elif hasattr(entry, 'updated'):
                        published = date_parser.parse(entry.updated)
                    
                    article = {
                        "title": entry.get('title', 'No title'),
                        "link": entry.get('link', ''),
                        "summary": entry.get('summary', entry.get('description', '')),
                        "published": published.isoformat() if published else None,
                        "source": feed.feed.get('title', 'Unknown'),
                        "author": entry.get('author', 'Unknown'),
                        "feed_url": feed_url,
                        "fetched_at": datetime.utcnow().isoformat(),
                    }
                    articles.append(article)
                except Exception as e:
                    logger.warning(f"Failed to parse entry from {feed_url}: {str(e)}")
                    continue
            
            logger.info(f"Fetched {len(articles)} articles from {feed_url}")
            return articles
            
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed {feed_url}: {str(e)}")
            return []
    
    async def fetch_from_feeds(
        self,
        category: Optional[str] = None,
        max_articles: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Fetch articles from configured RSS feeds.
        
        Args:
            category: Specific category or None for all
            max_articles: Maximum articles to fetch
            
        Returns:
            List of parsed articles
        """
        feeds_to_fetch = []
        
        if category and category in self.feeds:
            feeds_to_fetch = self.feeds[category]
        elif category is None:
            # Fetch from all categories
            for category_feeds in self.feeds.values():
                feeds_to_fetch.extend(category_feeds)
        else:
            logger.warning(f"Unknown category: {category}")
            return []
        
        # Fetch feeds in parallel using thread pool
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(self.executor, self._parse_feed, feed_url)
            for feed_url in feeds_to_fetch
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten results and handle exceptions
        all_articles = []
        for result in results:
            if isinstance(result, list):
                all_articles.extend(result)
            elif isinstance(result, Exception):
                logger.error(f"Feed fetch error: {str(result)}")
        
        # Sort by published date (newest first)
        all_articles.sort(
            key=lambda x: x.get('published') or '', 
            reverse=True
        )
        
        return all_articles[:max_articles]
    
    def add_feed(self, feed_url: str, category: str = "custom"):
        """Add a new RSS feed to the aggregator."""
        if category not in self.feeds:
            self.feeds[category] = []
        if feed_url not in self.feeds[category]:
            self.feeds[category].append(feed_url)
            logger.info(f"Added feed {feed_url} to category {category}")
    
    def list_feeds(self) -> Dict[str, List[str]]:
        """List all configured feeds by category."""
        return self.feeds


class ArticleExtractor:
    """
    Extract full article content from URLs using newspaper3k.
    
    Downloads and parses article content, bypassing paywalls when possible.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0; +http://example.com/bot)'
        })
    
    def _extract_article(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract full article content from URL synchronously."""
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            # Try to extract additional metadata
            try:
                article.nlp()  # Natural language processing
            except:
                pass  # NLP might fail, that's okay
            
            return {
                "url": url,
                "title": article.title,
                "text": article.text,
                "summary": article.summary if hasattr(article, 'summary') else '',
                "authors": article.authors,
                "publish_date": article.publish_date.isoformat() if article.publish_date else None,
                "top_image": article.top_image,
                "images": list(article.images),
                "keywords": list(article.keywords) if hasattr(article, 'keywords') else [],
                "extracted_at": datetime.utcnow().isoformat(),
            }
            
        except Exception as e:
            logger.error(f"Failed to extract article from {url}: {str(e)}")
            return None
    
    async def extract_articles(
        self,
        urls: List[str],
        max_concurrent: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Extract full content from multiple article URLs.
        
        Args:
            urls: List of article URLs
            max_concurrent: Maximum concurrent extractions
            
        Returns:
            List of extracted articles
        """
        executor = ThreadPoolExecutor(max_workers=max_concurrent)
        loop = asyncio.get_event_loop()
        
        tasks = [
            loop.run_in_executor(executor, self._extract_article, url)
            for url in urls
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out None and exceptions
        articles = [
            result for result in results
            if result is not None and not isinstance(result, Exception)
        ]
        
        logger.info(f"Successfully extracted {len(articles)}/{len(urls)} articles")
        return articles


class HackerNewsClient:
    """
    Client for Hacker News API - completely free, no API key required.
    
    Fetches top stories and trending tech news.
    """
    
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    
    def __init__(self):
        self.session = requests.Session()
    
    def _fetch_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a single item from Hacker News."""
        try:
            response = self.session.get(
                f"{self.BASE_URL}/item/{item_id}.json",
                timeout=5
            )
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch HN item {item_id}: {str(e)}")
            return None
    
    async def fetch_top_stories(self, limit: int = 30) -> List[Dict[str, Any]]:
        """
        Fetch top stories from Hacker News.
        
        Args:
            limit: Number of stories to fetch
            
        Returns:
            List of story objects
        """
        try:
            # Get top story IDs
            response = self.session.get(f"{self.BASE_URL}/topstories.json")
            story_ids = response.json()[:limit]
            
            # Fetch stories in parallel
            executor = ThreadPoolExecutor(max_workers=10)
            loop = asyncio.get_event_loop()
            
            tasks = [
                loop.run_in_executor(executor, self._fetch_item, story_id)
                for story_id in story_ids
            ]
            
            results = await asyncio.gather(*tasks)
            
            # Filter and format stories
            stories = []
            for item in results:
                if item and item.get('type') == 'story':
                    stories.append({
                        "id": item.get('id'),
                        "title": item.get('title'),
                        "url": item.get('url', f"https://news.ycombinator.com/item?id={item.get('id')}"),
                        "score": item.get('score', 0),
                        "author": item.get('by'),
                        "time": datetime.fromtimestamp(item.get('time', 0)).isoformat(),
                        "comments": item.get('descendants', 0),
                        "source": "Hacker News",
                    })
            
            logger.info(f"Fetched {len(stories)} stories from Hacker News")
            return stories
            
        except Exception as e:
            logger.error(f"Failed to fetch Hacker News stories: {str(e)}")
            return []


class NewsDataManager:
    """
    Manager for coordinating news data from multiple free sources.
    
    Combines data from:
    - RSS feeds (BBC, Guardian, TechCrunch, etc.)
    - Hacker News API
    - Full article extraction
    - User-uploaded newspapers (OCR processed)
    """
    
    def __init__(self):
        self.api_client = OpenSourceNewsClient()
        self.rss_aggregator = RSSFeedAggregator()
    
    async def fetch_all_news(
        self,
        category: str = None,
        language: str = "en",
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Fetch news from all available sources.
        
        Args:
            category: Category filter
            language: Language preference
            limit: Maximum total articles
            
        Returns:
            Combined list of articles from all sources
        """
        # Fetch from multiple sources concurrently
        api_task = self.api_client.fetch_latest_news(
            category=category,
            language=language,
            limit=limit // 2
        )
        
        rss_task = self.rss_aggregator.fetch_from_feeds(
            max_articles=limit // 2
        )
        
        # Wait for all sources
        api_results, rss_results = await asyncio.gather(
            api_task,
            rss_task,
            return_exceptions=True
        )
        
        # Combine results
        all_articles = []
        
        if not isinstance(api_results, Exception):
            all_articles.extend(api_results)
        
        if not isinstance(rss_results, Exception):
            all_articles.extend(rss_results)
        
        # Deduplicate by title/url
        seen = set()
        unique_articles = []
        
        for article in all_articles:
            identifier = (article.get('title'), article.get('url'))
            if identifier not in seen:
                seen.add(identifier)
                unique_articles.append(article)
        
        return unique_articles[:limit]
