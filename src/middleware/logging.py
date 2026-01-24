"""Logging middleware for FastAPI."""

import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from src.utils.logger import request_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next):
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Start timer
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000
            
            # Log request
            request_logger.log_request(
                method=request.method,
                path=str(request.url.path),
                status_code=response.status_code,
                duration_ms=duration_ms,
                request_id=request_id,
                ip_address=client_ip
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{duration_ms:.2f}ms"
            
            return response
        
        except Exception as e:
            # Log error
            request_logger.log_error(
                method=request.method,
                path=str(request.url.path),
                error=str(e),
                request_id=request_id
            )
            raise
