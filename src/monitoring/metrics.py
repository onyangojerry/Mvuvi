"""
Monitoring and metrics collection.
"""

import time
from functools import wraps
from typing import Callable, Dict, Any
from datetime import datetime
import logging

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from fastapi.responses import Response as FastAPIResponse

logger = logging.getLogger(__name__)


# Prometheus metrics
request_count = Counter(
    'vuva_requests_total',
    'Total request count',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'vuva_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

ocr_processing_time = Histogram(
    'vuva_ocr_processing_seconds',
    'OCR processing time in seconds',
    ['engine']
)

ocr_requests = Counter(
    'vuva_ocr_requests_total',
    'Total OCR requests',
    ['engine', 'status']
)

active_users = Gauge(
    'vuva_active_users',
    'Number of active users'
)

api_errors = Counter(
    'vuva_api_errors_total',
    'Total API errors',
    ['endpoint', 'error_type']
)

database_operations = Histogram(
    'vuva_database_operation_seconds',
    'Database operation duration',
    ['operation']
)

cache_hits = Counter(
    'vuva_cache_hits_total',
    'Cache hit count',
    ['cache_type']
)

cache_misses = Counter(
    'vuva_cache_misses_total',
    'Cache miss count',
    ['cache_type']
)


class MetricsCollector:
    """Centralized metrics collection."""
    
    def __init__(self):
        self.start_time = time.time()
        self.request_stats: Dict[str, Any] = {}
    
    def record_request(self, method: str, endpoint: str, status: int, duration: float):
        """Record a request."""
        request_count.labels(method=method, endpoint=endpoint, status=status).inc()
        request_duration.labels(method=method, endpoint=endpoint).observe(duration)
    
    def record_ocr_processing(self, engine: str, duration: float, status: str):
        """Record OCR processing."""
        ocr_processing_time.labels(engine=engine).observe(duration)
        ocr_requests.labels(engine=engine, status=status).inc()
    
    def record_error(self, endpoint: str, error_type: str):
        """Record an error."""
        api_errors.labels(endpoint=endpoint, error_type=error_type).inc()
    
    def record_database_operation(self, operation: str, duration: float):
        """Record database operation."""
        database_operations.labels(operation=operation).observe(duration)
    
    def record_cache_hit(self, cache_type: str):
        """Record cache hit."""
        cache_hits.labels(cache_type=cache_type).inc()
    
    def record_cache_miss(self, cache_type: str):
        """Record cache miss."""
        cache_misses.labels(cache_type=cache_type).inc()
    
    def update_active_users(self, count: int):
        """Update active user count."""
        active_users.set(count)
    
    def get_uptime(self) -> float:
        """Get service uptime in seconds."""
        return time.time() - self.start_time


# Global metrics collector
metrics_collector = MetricsCollector()


def track_api_call(endpoint_name: str):
    """
    Decorator to track API calls.
    
    Usage:
        @track_api_call("news_list")
        async def get_news():
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            status = 200
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                status = 500
                error_type = type(e).__name__
                metrics_collector.record_error(endpoint_name, error_type)
                logger.error(f"Error in {endpoint_name}: {str(e)}")
                raise
            finally:
                duration = time.time() - start_time
                metrics_collector.record_request(
                    method="GET",  # Would need to get from request
                    endpoint=endpoint_name,
                    status=status,
                    duration=duration
                )
        
        return wrapper
    return decorator


async def metrics_middleware(request: Request, call_next):
    """Middleware to collect metrics for all requests."""
    start_time = time.time()
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        metrics_collector.record_request(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code,
            duration=duration
        )
        
        # Add duration header
        response.headers["X-Process-Time"] = str(duration)
        
        return response
    
    except Exception as e:
        duration = time.time() - start_time
        metrics_collector.record_request(
            method=request.method,
            endpoint=request.url.path,
            status=500,
            duration=duration
        )
        metrics_collector.record_error(request.url.path, type(e).__name__)
        raise


async def get_metrics() -> FastAPIResponse:
    """
    Get Prometheus metrics.
    
    Usage:
        app.add_route("/metrics", get_metrics, methods=["GET"])
    """
    return FastAPIResponse(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


def get_health_metrics() -> Dict[str, Any]:
    """Get health metrics for detailed health check."""
    return {
        "uptime_seconds": metrics_collector.get_uptime(),
        "start_time": datetime.fromtimestamp(metrics_collector.start_time).isoformat(),
        "metrics": {
            "requests_total": "See /metrics endpoint",
            "active_users": "See /metrics endpoint",
            "errors_total": "See /metrics endpoint"
        }
    }
