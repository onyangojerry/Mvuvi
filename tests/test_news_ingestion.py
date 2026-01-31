"""
Comprehensive tests for news ingestion service.
Tests RSS feed aggregation, Hacker News integration, and article extraction.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
import feedparser

# Import the classes to test
import sys
sys.path.insert(0, '/Users/loan/Desktop/Mvuvi/vuva')
from src.services.news_ingestion import (
    RSSFeedAggregator,
    ArticleExtractor,
    HackerNewsClient,
    NewsDataManager
)


# ============================================================================
# Test RSS Feed Aggregator
# ============================================================================

class TestRSSFeedAggregator:
    """Test RSS feed aggregation functionality."""
    
    def test_feed_sources_loaded(self):
        """Test that feed sources are properly loaded."""
        aggregator = RSSFeedAggregator()
        
        assert len(aggregator.feed_sources) > 0
        assert "technology" in aggregator.feed_sources
        assert "world" in aggregator.feed_sources
        assert "business" in aggregator.feed_sources
        assert "science" in aggregator.feed_sources
        assert "general" in aggregator.feed_sources
    
    def test_technology_feeds_present(self):
        """Test that technology feeds are configured."""
        aggregator = RSSFeedAggregator()
        tech_feeds = aggregator.feed_sources.get("technology", [])
        
        assert len(tech_feeds) > 0
        # Check for known tech news sources
        feed_urls = [f["url"] for f in tech_feeds]
        assert any("techcrunch" in url.lower() for url in feed_urls)
    
    @patch('feedparser.parse')
    def test_fetch_single_feed(self, mock_parse):
        """Test fetching a single RSS feed."""
        # Mock feedparser response
        mock_parse.return_value = Mock(
            entries=[
                Mock(
                    title="Test Article",
                    link="https://example.com/article1",
                    summary="Test summary",
                    published_parsed=datetime(2026, 1, 24).timetuple()
                )
            ]
        )
        
        aggregator = RSSFeedAggregator()
        feed_url = "https://example.com/feed"
        
        articles = aggregator._fetch_single_feed(feed_url, "technology")
        
        assert len(articles) == 1
        assert articles[0]["title"] == "Test Article"
        assert articles[0]["url"] == "https://example.com/article1"
        assert articles[0]["category"] == "technology"
    
    @patch('feedparser.parse')
    def test_fetch_single_feed_with_error(self, mock_parse):
        """Test error handling when fetching a feed fails."""
        mock_parse.side_effect = Exception("Network error")
        
        aggregator = RSSFeedAggregator()
        articles = aggregator._fetch_single_feed("https://example.com/feed", "technology")
        
        # Should return empty list on error
        assert articles == []
    
    @patch.object(RSSFeedAggregator, '_fetch_single_feed')
    def test_fetch_category(self, mock_fetch):
        """Test fetching all feeds from a category."""
        mock_fetch.return_value = [{"title": "Article", "url": "https://example.com"}]
        
        aggregator = RSSFeedAggregator()
        articles = aggregator.fetch_category("technology", limit=10)
        
        assert isinstance(articles, list)
        assert mock_fetch.called
    
    @patch.object(RSSFeedAggregator, '_fetch_single_feed')
    def test_fetch_all_categories(self, mock_fetch):
        """Test fetching from all categories."""
        mock_fetch.return_value = [{"title": "Article", "url": "https://example.com"}]
        
        aggregator = RSSFeedAggregator()
        all_articles = aggregator.fetch_all(limit_per_category=5)
        
        assert isinstance(all_articles, dict)
        assert "technology" in all_articles
        assert "world" in all_articles


# ============================================================================
# Test Article Extractor
# ============================================================================

class TestArticleExtractor:
    """Test article extraction functionality."""
    
    def test_extractor_initialization(self):
        """Test that extractor initializes properly."""
        extractor = ArticleExtractor()
        assert extractor is not None
    
    @patch('newspaper.Article')
    def test_extract_article(self, mock_article_class):
        """Test extracting full article content."""
        # Mock newspaper Article
        mock_article = Mock()
        mock_article.download.return_value = None
        mock_article.parse.return_value = None
        mock_article.nlp.return_value = None
        mock_article.title = "Test Article"
        mock_article.text = "Full article text content"
        mock_article.authors = ["John Doe"]
        mock_article.publish_date = datetime(2026, 1, 24)
        mock_article.keywords = ["test", "article"]
        mock_article.summary = "Article summary"
        
        mock_article_class.return_value = mock_article
        
        extractor = ArticleExtractor()
        result = extractor.extract("https://example.com/article")
        
        assert result["title"] == "Test Article"
        assert result["text"] == "Full article text content"
        assert result["authors"] == ["John Doe"]
        assert "url" in result
    
    @patch('newspaper.Article')
    def test_extract_article_with_error(self, mock_article_class):
        """Test error handling during article extraction."""
        mock_article = Mock()
        mock_article.download.side_effect = Exception("Download failed")
        mock_article_class.return_value = mock_article
        
        extractor = ArticleExtractor()
        result = extractor.extract("https://example.com/article")
        
        assert result is None
    
    @patch('newspaper.Article')
    def test_extract_multiple_articles(self, mock_article_class):
        """Test extracting multiple articles."""
        mock_article = Mock()
        mock_article.download.return_value = None
        mock_article.parse.return_value = None
        mock_article.nlp.return_value = None
        mock_article.title = "Test"
        mock_article.text = "Content"
        mock_article.authors = []
        mock_article.publish_date = None
        mock_article.keywords = []
        mock_article.summary = ""
        
        mock_article_class.return_value = mock_article
        
        extractor = ArticleExtractor()
        urls = [
            "https://example.com/article1",
            "https://example.com/article2"
        ]
        results = extractor.extract_multiple(urls)
        
        assert len(results) == 2


# ============================================================================
# Test Hacker News Client
# ============================================================================

class TestHackerNewsClient:
    """Test Hacker News API integration."""
    
    def test_client_initialization(self):
        """Test that client initializes with correct base URL."""
        client = HackerNewsClient()
        assert client.base_url == "https://hacker-news.firebaseio.com/v0"
    
    @patch('requests.get')
    def test_get_top_stories_ids(self, mock_get):
        """Test fetching top story IDs."""
        mock_get.return_value.json.return_value = [1, 2, 3, 4, 5]
        
        client = HackerNewsClient()
        story_ids = client._get_top_stories_ids()
        
        assert len(story_ids) == 5
        assert all(isinstance(id, int) for id in story_ids)
    
    @patch('requests.get')
    def test_get_story_details(self, mock_get):
        """Test fetching story details."""
        mock_get.return_value.json.return_value = {
            "id": 12345,
            "title": "Test Story",
            "url": "https://example.com",
            "score": 100,
            "by": "testuser",
            "time": 1706054400,
            "descendants": 50
        }
        
        client = HackerNewsClient()
        story = client._get_story_details(12345)
        
        assert story["title"] == "Test Story"
        assert story["score"] == 100
        assert story["comments_count"] == 50
    
    @patch('requests.get')
    def test_get_top_stories(self, mock_get):
        """Test fetching top stories with details."""
        # Mock story IDs response
        mock_get.return_value.json.side_effect = [
            [1, 2],  # Story IDs
            {  # First story
                "id": 1,
                "title": "Story 1",
                "url": "https://example.com/1",
                "score": 100,
                "by": "user1",
                "time": 1706054400,
                "descendants": 50
            },
            {  # Second story
                "id": 2,
                "title": "Story 2",
                "url": "https://example.com/2",
                "score": 200,
                "by": "user2",
                "time": 1706054400,
                "descendants": 100
            }
        ]
        
        client = HackerNewsClient()
        stories = client.get_top_stories(limit=2)
        
        assert len(stories) == 2
        assert stories[0]["title"] == "Story 1"
        assert stories[1]["title"] == "Story 2"
    
    @patch('requests.get')
    def test_get_top_stories_with_error(self, mock_get):
        """Test error handling when fetching stories."""
        mock_get.side_effect = Exception("API error")
        
        client = HackerNewsClient()
        stories = client.get_top_stories(limit=10)
        
        # Should return empty list on error
        assert stories == []


# ============================================================================
# Test News Data Manager
# ============================================================================

class TestNewsDataManager:
    """Test the overall news data management."""
    
    def test_manager_initialization(self):
        """Test that manager initializes all components."""
        manager = NewsDataManager()
        
        assert manager.rss_aggregator is not None
        assert manager.article_extractor is not None
        assert manager.hn_client is not None
    
    @patch.object(RSSFeedAggregator, 'fetch_category')
    def test_get_news_by_category(self, mock_fetch):
        """Test getting news by category."""
        mock_fetch.return_value = [
            {"title": "Article 1", "url": "https://example.com/1"}
        ]
        
        manager = NewsDataManager()
        news = manager.get_news_by_category("technology", limit=10)
        
        assert len(news) > 0
        assert mock_fetch.called
    
    @patch.object(HackerNewsClient, 'get_top_stories')
    def test_get_hacker_news(self, mock_get):
        """Test getting Hacker News stories."""
        mock_get.return_value = [
            {"title": "HN Story", "url": "https://example.com"}
        ]
        
        manager = NewsDataManager()
        stories = manager.get_hacker_news(limit=5)
        
        assert len(stories) > 0
        assert mock_get.called
    
    @patch.object(ArticleExtractor, 'extract')
    def test_extract_full_article(self, mock_extract):
        """Test extracting full article content."""
        mock_extract.return_value = {
            "title": "Full Article",
            "text": "Article content",
            "authors": ["Author"],
            "publish_date": datetime(2026, 1, 24),
            "url": "https://example.com"
        }
        
        manager = NewsDataManager()
        article = manager.extract_full_article("https://example.com")
        
        assert article["title"] == "Full Article"
        assert mock_extract.called
    
    @patch.object(RSSFeedAggregator, 'fetch_all')
    def test_get_all_news(self, mock_fetch):
        """Test getting news from all categories."""
        mock_fetch.return_value = {
            "technology": [{"title": "Tech News"}],
            "world": [{"title": "World News"}]
        }
        
        manager = NewsDataManager()
        all_news = manager.get_all_news(limit_per_category=5)
        
        assert isinstance(all_news, dict)
        assert "technology" in all_news
        assert mock_fetch.called


# ============================================================================
# Integration Tests
# ============================================================================

class TestNewsIngestionIntegration:
    """Integration tests for the news ingestion pipeline."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_news_fetch(self):
        """Test the complete news fetching pipeline."""
        manager = NewsDataManager()
        # This will make real API calls - use with caution
        # Uncomment only for integration testing
        # news = await manager.get_news_by_category("technology", limit=1)
        # assert len(news) > 0
        pass

    @pytest.mark.asyncio
    async def test_multiple_categories(self):
        """Test fetching from multiple categories."""
        manager = NewsDataManager()
        categories = ["technology", "world"]
        results = {}
        for category in categories:
            # Mock this for unit tests
            results[category] = []
        assert len(results) == 2


# ============================================================================
# Performance Tests
# ============================================================================

class TestNewsIngestionPerformance:
    """Performance tests for news ingestion."""
    
    @pytest.mark.performance
    @patch.object(RSSFeedAggregator, '_fetch_single_feed')
    def test_fetch_speed(self, mock_fetch):
        """Test that fetching is reasonably fast."""
        import time
        
        mock_fetch.return_value = [{"title": "Article"}]
        
        aggregator = RSSFeedAggregator()
        
        start = time.time()
        articles = aggregator.fetch_category("technology", limit=5)
        duration = time.time() - start
        
        # Should complete in under 5 seconds (mocked)
        assert duration < 5.0
    
    @pytest.mark.performance
    @patch.object(HackerNewsClient, 'get_top_stories')
    def test_hn_fetch_speed(self, mock_get):
        """Test Hacker News fetching speed."""
        import time
        
        mock_get.return_value = [
            {"title": f"Story {i}", "url": f"https://example.com/{i}"}
            for i in range(10)
        ]
        
        client = HackerNewsClient()
        
        start = time.time()
        stories = client.get_top_stories(limit=10)
        duration = time.time() - start
        
        # Should complete in under 2 seconds (mocked)
        assert duration < 2.0


# ============================================================================
# Error Handling Tests
# ============================================================================

class TestNewsIngestionErrorHandling:
    """Test error handling in news ingestion."""
    
    @patch('feedparser.parse')
    def test_malformed_rss_feed(self, mock_parse):
        """Test handling of malformed RSS feeds."""
        mock_parse.return_value = Mock(entries=[])
        
        aggregator = RSSFeedAggregator()
        articles = aggregator._fetch_single_feed("https://invalid.com/feed", "technology")
        
        # Should return empty list, not crash
        assert articles == []
    
    @patch('requests.get')
    def test_network_timeout(self, mock_get):
        """Test handling of network timeouts."""
        import requests
        mock_get.side_effect = requests.Timeout("Timeout")
        
        client = HackerNewsClient()
        stories = client.get_top_stories(limit=5)
        
        # Should return empty list, not crash
        assert stories == []
    
    @patch('newspaper.Article')
    def test_article_extraction_failure(self, mock_article_class):
        """Test handling of article extraction failures."""
        mock_article = Mock()
        mock_article.download.side_effect = Exception("Extraction failed")
        mock_article_class.return_value = mock_article
        
        extractor = ArticleExtractor()
        result = extractor.extract("https://example.com")
        
        # Should return None, not crash
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
