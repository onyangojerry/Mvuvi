"""
Comprehensive test suite for Redis caching service.

Tests cover:
- Basic get/set/delete operations
- TTL (Time To Live) functionality
- Connection failure handling
- Cache statistics
- Pattern-based deletion
- Decorator caching
"""

import pytest
import time
from datetime import timedelta

from src.services.cache_service import CacheService, get_cache_service


class TestCacheBasicOperations:
    """Test basic cache operations."""
    
    def setup_method(self):
        """Set up test cache service."""
        self.cache = get_cache_service()
        self.cache.clear_all()  # Clean slate for each test
    
    def test_set_and_get_string(self):
        """Test setting and getting string values."""
        key = "test:string"
        value = "Hello, World!"
        
        # Set value
        assert self.cache.set(key, value) is True
        
        # Get value
        retrieved = self.cache.get(key)
        assert retrieved == value
    
    def test_set_and_get_dict(self):
        """Test setting and getting dictionary values."""
        key = "test:dict"
        value = {"name": "John", "age": 30, "active": True}
        
        assert self.cache.set(key, value) is True
        retrieved = self.cache.get(key)
        
        assert retrieved == value
        assert retrieved["name"] == "John"
        assert retrieved["age"] == 30
        assert retrieved["active"] is True
    
    def test_set_and_get_list(self):
        """Test setting and getting list values."""
        key = "test:list"
        value = [1, 2, 3, "four", 5.0]
        
        assert self.cache.set(key, value) is True
        retrieved = self.cache.get(key)
        
        assert retrieved == value
        assert len(retrieved) == 5
    
    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist."""
        result = self.cache.get("nonexistent:key")
        assert result is None
    
    def test_delete_key(self):
        """Test deleting a key."""
        key = "test:delete"
        value = "will be deleted"
        
        # Set and verify
        self.cache.set(key, value)
        assert self.cache.get(key) == value
        
        # Delete
        assert self.cache.delete(key) is True
        
        # Verify deleted
        assert self.cache.get(key) is None
    
    def test_delete_nonexistent_key(self):
        """Test deleting a key that doesn't exist."""
        result = self.cache.delete("nonexistent:key")
        assert result is False
    
    def test_exists_key(self):
        """Test checking if key exists."""
        key = "test:exists"
        
        # Key doesn't exist initially
        assert self.cache.exists(key) is False
        
        # Set key
        self.cache.set(key, "value")
        
        # Key should exist now
        assert self.cache.exists(key) is True
        
        # Delete key
        self.cache.delete(key)
        
        # Key shouldn't exist anymore
        assert self.cache.exists(key) is False


class TestCacheTTL:
    """Test TTL (Time To Live) functionality."""
    
    def setup_method(self):
        """Set up test cache service."""
        self.cache = get_cache_service()
        self.cache.clear_all()
    
    def test_set_with_ttl_seconds(self):
        """Test setting value with TTL in seconds."""
        key = "test:ttl:seconds"
        value = "expires in 2 seconds"
        
        # Set with 2 second TTL
        self.cache.set(key, value, ttl=2)
        
        # Should exist immediately
        assert self.cache.get(key) == value
        
        # Wait for expiration
        time.sleep(2.5)
        
        # Should be expired
        assert self.cache.get(key) is None
    
    def test_set_with_ttl_timedelta(self):
        """Test setting value with TTL as timedelta."""
        key = "test:ttl:timedelta"
        value = "expires in 2 seconds"
        
        # Set with timedelta
        self.cache.set(key, value, ttl=timedelta(seconds=2))
        
        # Should exist immediately
        assert self.cache.get(key) == value
        
        # Wait for expiration
        time.sleep(2.5)
        
        # Should be expired
        assert self.cache.get(key) is None
    
    def test_set_without_ttl(self):
        """Test setting value without TTL (persists)."""
        key = "test:no:ttl"
        value = "persists forever"
        
        self.cache.set(key, value)
        
        # Should exist
        assert self.cache.get(key) == value
        
        # Wait a bit
        time.sleep(1)
        
        # Should still exist
        assert self.cache.get(key) == value


class TestCachePatterns:
    """Test pattern-based operations."""
    
    def setup_method(self):
        """Set up test cache service."""
        self.cache = get_cache_service()
        self.cache.clear_all()
    
    def test_delete_pattern(self):
        """Test deleting keys by pattern."""
        # Set multiple keys with user: prefix
        self.cache.set("user:1", {"id": 1})
        self.cache.set("user:2", {"id": 2})
        self.cache.set("user:3", {"id": 3})
        self.cache.set("post:1", {"id": 1})
        
        # Delete all user: keys
        deleted = self.cache.delete_pattern("user:*")
        
        assert deleted == 3
        
        # Verify user keys deleted
        assert self.cache.get("user:1") is None
        assert self.cache.get("user:2") is None
        assert self.cache.get("user:3") is None
        
        # Verify post key still exists
        assert self.cache.get("post:1") is not None
    
    def test_delete_pattern_no_matches(self):
        """Test deleting pattern with no matches."""
        deleted = self.cache.delete_pattern("nonexistent:*")
        assert deleted == 0


class TestCacheStatistics:
    """Test cache statistics and monitoring."""
    
    def setup_method(self):
        """Set up test cache service with fresh stats."""
        self.cache = get_cache_service()
        self.cache.clear_all()
        # Reset stats by creating new instance
        self.cache._hits = 0
        self.cache._misses = 0
        self.cache._errors = 0
    
    def test_hit_statistics(self):
        """Test cache hit statistics."""
        key = "test:stats:hit"
        
        # Set value
        self.cache.set(key, "value")
        
        # Get value (should be a hit)
        self.cache.get(key)
        self.cache.get(key)
        
        stats = self.cache.get_stats()
        assert stats["hits"] >= 2
    
    def test_miss_statistics(self):
        """Test cache miss statistics."""
        # Get non-existent keys
        self.cache.get("nonexistent:1")
        self.cache.get("nonexistent:2")
        
        stats = self.cache.get_stats()
        assert stats["misses"] >= 2
    
    def test_hit_rate_calculation(self):
        """Test hit rate percentage calculation."""
        key = "test:stats:rate"
        
        # Set value
        self.cache.set(key, "value")
        
        # 3 hits
        self.cache.get(key)
        self.cache.get(key)
        self.cache.get(key)
        
        # 1 miss
        self.cache.get("nonexistent")
        
        stats = self.cache.get_stats()
        
        # Hit rate should be 75% (3 hits out of 4 requests)
        assert stats["total_requests"] >= 4
        assert stats["hit_rate_percentage"] > 50


class TestCacheHealthCheck:
    """Test cache health checking."""
    
    def setup_method(self):
        """Set up test cache service."""
        self.cache = get_cache_service()
    
    def test_health_check_when_healthy(self):
        """Test health check when Redis is healthy."""
        is_healthy = self.cache.health_check()
        assert is_healthy is True
    
    def test_cache_stats_include_redis_info(self):
        """Test that stats include Redis information."""
        stats = self.cache.get_stats()
        
        assert "enabled" in stats
        assert "hits" in stats
        assert "misses" in stats
        
        if stats["enabled"]:
            # Should have Redis-specific stats
            assert "used_memory_human" in stats or "total_connections_received" in stats


class TestCacheKeyHashing:
    """Test cache key generation utilities."""
    
    def setup_method(self):
        """Set up test cache service."""
        self.cache = get_cache_service()
    
    def test_hash_key_single_argument(self):
        """Test hashing single argument."""
        hash1 = self.cache.hash_key("test")
        hash2 = self.cache.hash_key("test")
        
        # Same input should produce same hash
        assert hash1 == hash2
        
        # Different input should produce different hash
        hash3 = self.cache.hash_key("different")
        assert hash1 != hash3
    
    def test_hash_key_multiple_arguments(self):
        """Test hashing multiple arguments."""
        hash1 = self.cache.hash_key("user", 123, "profile")
        hash2 = self.cache.hash_key("user", 123, "profile")
        
        assert hash1 == hash2
        
        # Different order should produce different hash
        hash3 = self.cache.hash_key(123, "user", "profile")
        assert hash1 != hash3
    
    def test_hash_key_with_objects(self):
        """Test hashing with different object types."""
        hash1 = self.cache.hash_key({"id": 1}, [1, 2, 3], True)
        hash2 = self.cache.hash_key({"id": 1}, [1, 2, 3], True)
        
        assert hash1 == hash2


class TestCacheDecorator:
    """Test cache decorator functionality."""
    
    def setup_method(self):
        """Set up test cache service."""
        self.cache = get_cache_service()
        self.cache.clear_all()
        self.call_count = 0
    
    def test_decorator_caches_results(self):
        """Test that decorator caches function results."""
        
        @self.cache.cache_result("test_func", ttl=60)
        def expensive_function(x, y):
            self.call_count += 1
            return x + y
        
        # First call
        result1 = expensive_function(5, 3)
        assert result1 == 8
        assert self.call_count == 1
        
        # Second call with same args (should use cache)
        result2 = expensive_function(5, 3)
        assert result2 == 8
        assert self.call_count == 1  # Not incremented
        
        # Third call with different args (should execute)
        result3 = expensive_function(10, 20)
        assert result3 == 30
        assert self.call_count == 2


class TestCacheGracefulDegradation:
    """Test cache behavior when Redis is unavailable."""
    
    def test_operations_when_disabled(self):
        """Test that operations don't crash when cache is disabled."""
        cache = CacheService()
        cache._enabled = False
        cache._client = None
        
        # Should return False/None but not crash
        assert cache.set("key", "value") is False
        assert cache.get("key") is None
        assert cache.delete("key") is False
        assert cache.exists("key") is False
        assert cache.delete_pattern("*") == 0
        assert cache.health_check() is False


class TestCacheNamespacing:
    """Test cache key namespacing."""
    
    def setup_method(self):
        """Set up test cache service."""
        self.cache = get_cache_service()
    
    def test_keys_have_namespace(self):
        """Test that all keys are namespaced with 'vuva:' prefix."""
        key = "test:namespace"
        self.cache.set(key, "value")
        
        # The actual key in Redis should have vuva: prefix
        generated_key = self.cache._generate_key(key)
        assert generated_key.startswith("vuva:")


class TestCacheComplexData:
    """Test caching complex data structures."""
    
    def setup_method(self):
        """Set up test cache service."""
        self.cache = get_cache_service()
        self.cache.clear_all()
    
    def test_cache_nested_dict(self):
        """Test caching nested dictionaries."""
        key = "test:nested"
        value = {
            "user": {
                "id": 1,
                "name": "John",
                "preferences": {
                    "theme": "dark",
                    "notifications": True
                }
            },
            "metadata": {
                "created": "2026-01-24",
                "tags": ["important", "verified"]
            }
        }
        
        self.cache.set(key, value)
        retrieved = self.cache.get(key)
        
        assert retrieved == value
        assert retrieved["user"]["preferences"]["theme"] == "dark"
        assert "verified" in retrieved["metadata"]["tags"]
    
    def test_cache_list_of_dicts(self):
        """Test caching list of dictionaries."""
        key = "test:list:dicts"
        value = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"}
        ]
        
        self.cache.set(key, value)
        retrieved = self.cache.get(key)
        
        assert retrieved == value
        assert len(retrieved) == 3
        assert retrieved[1]["name"] == "Item 2"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
