"""
Redis caching service for Vuva API.

Provides high-performance caching with TTL support, graceful degradation,
and comprehensive monitoring.
"""

import json
import hashlib
from typing import Optional, Any, Union
from datetime import timedelta
import logging

import redis
from redis.connection import ConnectionPool
from redis.exceptions import RedisError, ConnectionError as RedisConnectionError

from src.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class CacheService:
    """
    Redis-backed caching service with graceful degradation.
    
    Features:
    - Connection pooling for performance
    - Automatic serialization/deserialization
    - TTL (Time To Live) support
    - Graceful degradation if Redis unavailable
    - Cache hit/miss metrics
    """
    
    def __init__(self):
        """Initialize Redis connection pool."""
        self._pool: Optional[ConnectionPool] = None
        self._client: Optional[redis.Redis] = None
        self._enabled = True
        self._hits = 0
        self._misses = 0
        self._errors = 0
        
        self._initialize_connection()
    
    def _initialize_connection(self) -> None:
        """Initialize Redis connection pool with error handling."""
        try:
            redis_url = getattr(settings, 'REDIS_URL', 'redis://localhost:6379/0')
            max_connections = getattr(settings, 'REDIS_MAX_CONNECTIONS', 50)
            
            self._pool = ConnectionPool.from_url(
                redis_url,
                max_connections=max_connections,
                decode_responses=False,  # We'll handle encoding
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True
            )
            
            self._client = redis.Redis(connection_pool=self._pool)
            
            # Test connection
            self._client.ping()
            logger.info(f"✅ Redis connected: {redis_url}")
            
        except (RedisError, RedisConnectionError) as e:
            logger.warning(f"⚠️  Redis unavailable: {e}. Caching disabled.")
            self._enabled = False
            self._client = None
    
    def _serialize(self, value: Any) -> bytes:
        """Serialize value to bytes for Redis storage."""
        return json.dumps(value, default=str).encode('utf-8')
    
    def _deserialize(self, value: bytes) -> Any:
        """Deserialize bytes from Redis to Python object."""
        if value is None:
            return None
        return json.loads(value.decode('utf-8'))
    
    def _generate_key(self, key: str) -> str:
        """
        Generate cache key with namespace prefix.
        
        Args:
            key: Base cache key
            
        Returns:
            Namespaced cache key
        """
        return f"vuva:{key}"
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        if not self._enabled or not self._client:
            return None
        
        try:
            cache_key = self._generate_key(key)
            value = self._client.get(cache_key)
            
            if value is not None:
                self._hits += 1
                logger.debug(f"Cache HIT: {key}")
                return self._deserialize(value)
            else:
                self._misses += 1
                logger.debug(f"Cache MISS: {key}")
                return None
                
        except RedisError as e:
            self._errors += 1
            logger.error(f"Cache GET error for key '{key}': {e}")
            return None
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[Union[int, timedelta]] = None
    ) -> bool:
        """
        Set value in cache with optional TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds or timedelta
            
        Returns:
            True if successful, False otherwise
        """
        if not self._enabled or not self._client:
            return False
        
        try:
            cache_key = self._generate_key(key)
            serialized_value = self._serialize(value)
            
            # Convert timedelta to seconds
            if isinstance(ttl, timedelta):
                ttl = int(ttl.total_seconds())
            
            if ttl:
                self._client.setex(cache_key, ttl, serialized_value)
            else:
                self._client.set(cache_key, serialized_value)
            
            logger.debug(f"Cache SET: {key} (TTL: {ttl}s)")
            return True
            
        except RedisError as e:
            self._errors += 1
            logger.error(f"Cache SET error for key '{key}': {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False otherwise
        """
        if not self._enabled or not self._client:
            return False
        
        try:
            cache_key = self._generate_key(key)
            result = self._client.delete(cache_key)
            logger.debug(f"Cache DELETE: {key}")
            return result > 0
            
        except RedisError as e:
            self._errors += 1
            logger.error(f"Cache DELETE error for key '{key}': {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if exists, False otherwise
        """
        if not self._enabled or not self._client:
            return False
        
        try:
            cache_key = self._generate_key(key)
            return bool(self._client.exists(cache_key))
            
        except RedisError as e:
            self._errors += 1
            logger.error(f"Cache EXISTS error for key '{key}': {e}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching pattern.
        
        Args:
            pattern: Key pattern (e.g., "user:*")
            
        Returns:
            Number of keys deleted
        """
        if not self._enabled or not self._client:
            return 0
        
        try:
            cache_pattern = self._generate_key(pattern)
            keys = self._client.keys(cache_pattern)
            
            if keys:
                deleted = self._client.delete(*keys)
                logger.info(f"Cache DELETE pattern '{pattern}': {deleted} keys")
                return deleted
            
            return 0
            
        except RedisError as e:
            self._errors += 1
            logger.error(f"Cache DELETE pattern error for '{pattern}': {e}")
            return 0
    
    def clear_all(self) -> bool:
        """
        Clear all cache entries (use with caution).
        
        Returns:
            True if successful, False otherwise
        """
        if not self._enabled or not self._client:
            return False
        
        try:
            # Only delete keys with our namespace
            deleted = self.delete_pattern("*")
            logger.warning(f"Cache CLEARED: {deleted} keys deleted")
            return True
            
        except RedisError as e:
            self._errors += 1
            logger.error(f"Cache CLEAR error: {e}")
            return False
    
    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with cache stats
        """
        total_requests = self._hits + self._misses
        hit_rate = (self._hits / total_requests * 100) if total_requests > 0 else 0
        
        stats = {
            "enabled": self._enabled,
            "hits": self._hits,
            "misses": self._misses,
            "errors": self._errors,
            "total_requests": total_requests,
            "hit_rate_percentage": round(hit_rate, 2)
        }
        
        # Add Redis info if available
        if self._enabled and self._client:
            try:
                info = self._client.info('stats')
                stats.update({
                    "total_connections_received": info.get('total_connections_received', 0),
                    "total_commands_processed": info.get('total_commands_processed', 0),
                    "instantaneous_ops_per_sec": info.get('instantaneous_ops_per_sec', 0),
                    "used_memory_human": self._client.info('memory').get('used_memory_human', 'N/A')
                })
            except RedisError:
                pass
        
        return stats
    
    def health_check(self) -> bool:
        """
        Check if Redis is healthy and responding.
        
        Returns:
            True if healthy, False otherwise
        """
        if not self._enabled or not self._client:
            return False
        
        try:
            return self._client.ping()
        except RedisError:
            return False
    
    def hash_key(self, *args: Any) -> str:
        """
        Generate a hash key from multiple arguments.
        Useful for caching function results.
        
        Args:
            *args: Arguments to hash
            
        Returns:
            MD5 hash string
        """
        combined = "|".join(str(arg) for arg in args)
        return hashlib.md5(combined.encode()).hexdigest()
    
    def cache_result(
        self,
        key_prefix: str,
        ttl: Optional[int] = None
    ):
        """
        Decorator to cache function results.
        
        Usage:
            @cache_service.cache_result("ocr", ttl=3600)
            def extract_text(image_path):
                # expensive operation
                return text
        
        Args:
            key_prefix: Prefix for cache key
            ttl: Time to live in seconds
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                # Generate cache key from function arguments
                cache_key = f"{key_prefix}:{self.hash_key(*args, **kwargs)}"
                
                # Try to get from cache
                cached = self.get(cache_key)
                if cached is not None:
                    return cached
                
                # Execute function
                result = func(*args, **kwargs)
                
                # Cache result
                self.set(cache_key, result, ttl)
                
                return result
            
            return wrapper
        return decorator
    
    def close(self) -> None:
        """Close Redis connection pool."""
        if self._pool:
            self._pool.disconnect()
            logger.info("Redis connection pool closed")


# Global cache service instance
_cache_service: Optional[CacheService] = None


def get_cache_service() -> CacheService:
    """
    Get global cache service instance (singleton pattern).
    
    Returns:
        CacheService instance
    """
    global _cache_service
    
    if _cache_service is None:
        _cache_service = CacheService()
    
    return _cache_service


# Convenience aliases
cache = get_cache_service()
