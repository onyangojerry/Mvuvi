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


# Additional utility functions for test compatibility and extended functionality

def sanitize_input(text: Optional[str], max_length: int = 1000) -> str:
    """
    Sanitize general text input.
    
    Enhanced sanitization that removes XSS, command injection, and other attacks.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        Sanitized text string
    """
    if text is None:
        return ""
    
    text = str(text)
    
    # Normalize Unicode to prevent fullwidth character attacks
    import unicodedata
    text = unicodedata.normalize('NFKC', text)
    
    # Use the existing sanitize_text_input as a base
    text = security_validator.sanitize_text_input(text, max_length)
    
    # Additional XSS protection - remove dangerous attributes
    dangerous_attributes = ['onerror', 'onload', 'onclick', 'onmouseover', 'onfocus']
    for attr in dangerous_attributes:
        # Remove the attribute and its value
        import re
        text = re.sub(rf'{attr}\s*=\s*["\']?[^"\'>]*["\']?', '', text, flags=re.IGNORECASE)
    
    # Command injection protection - remove shell metacharacters
    dangerous_chars = [';', '|', '&', '$', '`', '\n', '\r']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal.
    
    Wrapper around SecurityValidator.sanitize_filename for convenience.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    return security_validator.sanitize_filename(filename)


def sanitize_sql_input(text: str) -> str:
    """
    Sanitize input to prevent SQL injection.
    
    Note: This is a defense-in-depth measure. The primary defense
    against SQL injection is using parameterized queries (SQLAlchemy ORM).
    
    Args:
        text: Input text that might be used in SQL context
        
    Returns:
        Sanitized text with dangerous SQL patterns removed/escaped
    """
    if not text:
        return ""
    
    # Remove or escape SQL comment sequences
    text = text.replace("--", "")
    text = text.replace("/*", "").replace("*/", "")
    
    # Remove SQL keywords in dangerous contexts
    dangerous_patterns = [
        r'\bUNION\b',
        r'\bSELECT\b',
        r'\bINSERT\b',
        r'\bUPDATE\b',
        r'\bDELETE\b',
        r'\bDROP\b',
        r'\bEXEC\b',
        r'\bEXECUTE\b',
        r'\bWAITFOR\b',
        r'\bSLEEP\b',
    ]
    
    for pattern in dangerous_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Escape single quotes (parameterized queries handle this better)
    text = text.replace("'", "''")
    
    return text


def validate_file_type(filename: str, allowed_types: list) -> bool:
    """
    Validate file type based on extension.
    
    Args:
        filename: Name of file to validate
        allowed_types: List of allowed extensions (without dot)
        
    Returns:
        True if file type is allowed, False otherwise
    """
    if not filename or not allowed_types:
        return False
    
    # Convert to lowercase for case-insensitive comparison
    filename_lower = filename.lower()
    
    # Check for double extensions (e.g., file.pdf.exe)
    parts = filename_lower.split('.')
    if len(parts) > 2:
        # More than one extension - potential attack
        return False
    
    # Get file extension
    if '.' not in filename_lower:
        return False
    
    extension = filename_lower.rsplit('.', 1)[-1]
    
    # Check if extension is in allowed list
    return extension in [ext.lower() for ext in allowed_types]


def check_file_size(file_size: int, max_size: int = 10 * 1024 * 1024) -> bool:
    """
    Check if file size is within allowed limit.
    
    Args:
        file_size: Size of file in bytes
        max_size: Maximum allowed size in bytes (default: 10MB)
        
    Returns:
        True if file size is valid, False otherwise
    """
    if file_size <= 0:
        return False
    
    if file_size > max_size:
        return False
    
    return True


def validate_file_upload(
    filename: str,
    file_size: int,
    allowed_types: list = None,
    max_size: int = 10 * 1024 * 1024
) -> Dict[str, Any]:
    """
    Comprehensive file upload validation.
    
    Args:
        filename: Name of uploaded file
        file_size: Size of file in bytes
        allowed_types: List of allowed file extensions
        max_size: Maximum allowed file size in bytes
        
    Returns:
        Dictionary with validation result:
        {
            "valid": bool,
            "error": Optional[str],
            "sanitized_filename": str
        }
    """
    if allowed_types is None:
        allowed_types = ["jpg", "jpeg", "png", "pdf", "txt"]
    
    # Validate file type
    if not validate_file_type(filename, allowed_types):
        return {
            "valid": False,
            "error": f"File type not allowed. Allowed types: {', '.join(allowed_types)}",
            "sanitized_filename": None
        }
    
    # Validate file size
    if not check_file_size(file_size, max_size):
        return {
            "valid": False,
            "error": f"File size invalid. Maximum size: {max_size / 1024 / 1024}MB",
            "sanitized_filename": None
        }
    
    # Sanitize filename
    safe_filename = sanitize_filename(filename)
    
    return {
        "valid": True,
        "error": None,
        "sanitized_filename": safe_filename
    }


def prevent_path_traversal(path: str) -> str:
    """
    Prevent path traversal attacks in file paths.
    
    Args:
        path: Input path string
        
    Returns:
        Sanitized path with traversal sequences removed
    """
    if not path:
        return ""
    
    # Remove URL encoding
    import urllib.parse
    path = urllib.parse.unquote(path)
    
    # Remove parent directory references
    path = path.replace("..", "")
    path = path.replace("./", "")
    
    # Remove absolute path indicators
    path = path.lstrip("/")
    path = re.sub(r'^[a-zA-Z]:\\', '', path)  # Windows absolute paths
    
    # Remove any remaining dangerous patterns
    path = path.replace("\\", "/")  # Normalize separators
    
    # Take only the filename component
    path = path.split("/")[-1]
    
    return path


def validate_url(
    url: str,
    allowed_schemes: list = None,
    check_open_redirect: bool = False
) -> bool:
    """
    Validate URL for security.
    
    Args:
        url: URL string to validate
        allowed_schemes: List of allowed URL schemes (default: ['http', 'https'])
        check_open_redirect: Whether to check for open redirect patterns
        
    Returns:
        True if URL is valid and safe, False otherwise
    """
    if allowed_schemes is None:
        allowed_schemes = ['http', 'https']
    
    if not url:
        return False
    
    # Check for dangerous protocols
    dangerous_schemes = ['javascript', 'data', 'file', 'vbscript']
    url_lower = url.lower()
    
    for scheme in dangerous_schemes:
        if url_lower.startswith(f"{scheme}:"):
            return False
    
    # Parse URL
    from urllib.parse import urlparse
    
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    
    # Validate scheme
    if parsed.scheme not in allowed_schemes:
        return False
    
    # Check for open redirect patterns (multiple @ signs, suspicious userinfo)
    if check_open_redirect:
        if url.count('@') > 1:
            return False
        if parsed.username or parsed.password:
            # URLs with credentials might be suspicious
            return False
    
    # Validate hostname exists
    if not parsed.netloc:
        return False
    
    return True
