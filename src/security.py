"""
Security middleware and utilities for the Vuva API.

Implements:
- Input sanitization
- Rate limiting
- Security headers
- Request validation
- API key authentication
"""

import re
import hashlib
import secrets
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import HTTPException, Security, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

logger = logging.getLogger(__name__)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


class SecurityValidator:
    """Input validation and sanitization."""
    
    # Patterns for validation
    FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9_\-\.]+$')
    LANGUAGE_CODE_PATTERN = re.compile(r'^[a-z]{2,3}$')
    SAFE_STRING_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-_\.,!?]+$')
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent path traversal attacks.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove path components
        filename = filename.split('/')[-1].split('\\')[-1]
        
        # Remove dangerous characters
        filename = re.sub(r'[^\w\s\-\.]', '', filename)
        
        # Limit length
        if len(filename) > 255:
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
            filename = name[:250] + ('.' + ext if ext else '')
        
        return filename or 'unnamed_file'
    
    @staticmethod
    def validate_language_code(code: str) -> bool:
        """
        Validate language code format.
        
        Args:
            code: Language code (e.g., 'en', 'es')
            
        Returns:
            True if valid
        """
        return bool(SecurityValidator.LANGUAGE_CODE_PATTERN.match(code))
    
    @staticmethod
    def sanitize_text_input(text: str, max_length: int = 1000) -> str:
        """
        Sanitize text input to prevent injection attacks.
        
        Args:
            text: Input text
            max_length: Maximum allowed length
            
        Returns:
            Sanitized text
        """
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Limit length
        text = text[:max_length]
        
        # Remove potentially dangerous patterns
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    @staticmethod
    def validate_image_content(content: bytes, max_size: int = 10 * 1024 * 1024) -> None:
        """
        Validate image content.
        
        Args:
            content: Image bytes
            max_size: Maximum size in bytes
            
        Raises:
            HTTPException: If validation fails
        """
        if len(content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "EMPTY_FILE", "message": "Image file is empty"}
            )
        
        if len(content) > max_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail={
                    "code": "FILE_TOO_LARGE",
                    "message": f"File size exceeds {max_size / 1024 / 1024}MB limit",
                    "file_size": len(content)
                }
            )
        
        # Check magic bytes for common image formats
        magic_bytes = {
            b'\xff\xd8\xff': 'JPEG',
            b'\x89PNG\r\n\x1a\n': 'PNG',
            b'GIF87a': 'GIF',
            b'GIF89a': 'GIF',
            b'%PDF': 'PDF',
        }
        
        is_valid = any(content.startswith(magic) for magic in magic_bytes.keys())
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"code": "INVALID_IMAGE", "message": "File is not a valid image"}
            )


class APIKeyAuth:
    """API key authentication."""
    
    def __init__(self):
        self.api_keys: Dict[str, Dict[str, Any]] = {}
        self.security = HTTPBearer()
    
    def generate_api_key(self, user_id: str, tier: str = "free") -> str:
        """
        Generate a new API key.
        
        Args:
            user_id: User identifier
            tier: Subscription tier (free, basic, premium)
            
        Returns:
            API key string
        """
        # Generate secure random key
        raw_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        
        # Store key metadata
        self.api_keys[key_hash] = {
            "user_id": user_id,
            "tier": tier,
            "created_at": datetime.utcnow().isoformat(),
            "last_used": None,
            "requests_count": 0,
        }
        
        return f"vuva_{raw_key}"
    
    async def verify_api_key(
        self,
        credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
    ) -> Dict[str, Any]:
        """
        Verify API key from request.
        
        Args:
            credentials: HTTP authorization credentials
            
        Returns:
            API key metadata
            
        Raises:
            HTTPException: If key is invalid
        """
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "MISSING_API_KEY", "message": "API key is required"}
            )
        
        api_key = credentials.credentials
        
        # Validate format
        if not api_key.startswith("vuva_"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "INVALID_API_KEY", "message": "Invalid API key format"}
            )
        
        # Hash and lookup
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        key_metadata = self.api_keys.get(key_hash)
        
        if not key_metadata:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": "INVALID_API_KEY", "message": "API key not found"}
            )
        
        # Update usage
        key_metadata["last_used"] = datetime.utcnow().isoformat()
        key_metadata["requests_count"] += 1
        
        return key_metadata


class SecurityHeaders:
    """Add security headers to responses."""
    
    @staticmethod
    def add_headers(response) -> None:
        """
        Add security headers to HTTP response.
        
        Args:
            response: HTTP response object
        """
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Enable XSS protection
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Content Security Policy
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self';"
        )
        
        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions Policy
        response.headers["Permissions-Policy"] = (
            "geolocation=(), "
            "microphone=(), "
            "camera=()"
        )


class RateLimitTiers:
    """Rate limit configurations by tier."""
    
    FREE_TIER = "100/hour"
    BASIC_TIER = "1000/hour"
    PREMIUM_TIER = "10000/hour"
    ADMIN_TIER = "100000/hour"
    
    @staticmethod
    def get_limit_for_tier(tier: str) -> str:
        """Get rate limit string for tier."""
        limits = {
            "free": RateLimitTiers.FREE_TIER,
            "basic": RateLimitTiers.BASIC_TIER,
            "premium": RateLimitTiers.PREMIUM_TIER,
            "admin": RateLimitTiers.ADMIN_TIER,
        }
        return limits.get(tier, RateLimitTiers.FREE_TIER)


def log_security_event(
    event_type: str,
    request: Request,
    details: Optional[Dict[str, Any]] = None
) -> None:
    """
    Log security-related events.
    
    Args:
        event_type: Type of security event
        request: HTTP request object
        details: Additional event details
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "client_ip": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("user-agent", "unknown"),
        "path": str(request.url.path),
        "method": request.method,
        "details": details or {}
    }
    
    logger.warning(f"Security Event: {log_entry}")


# Singleton instances
security_validator = SecurityValidator()
api_key_auth = APIKeyAuth()
