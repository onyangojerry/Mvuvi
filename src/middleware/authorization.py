"""
Authorization middleware for role-based access control (RBAC).
"""

from typing import List, Optional, Callable
from functools import wraps
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.services.permission_service import PermissionService

security = HTTPBearer()


# Role definitions with permissions
ROLES = {
    "free": {
        "permissions": [
            "read:news",
            "read:sources"
        ],
        "rate_limit": 100,  # per hour
    },
    "basic": {
        "permissions": [
            "read:news",
            "read:sources",
            "read:full_articles",
            "write:preferences"
        ],
        "rate_limit": 1000,
    },
    "premium": {
        "permissions": [
            "read:news",
            "read:sources",
            "read:full_articles",
            "write:preferences",
            "read:analytics",
            "unlimited:ocr"
        ],
        "rate_limit": 10000,
    },
    "admin": {
        "permissions": ["*"],  # All permissions
        "rate_limit": None,  # No limit
    }
}


def get_user_role(request: Request) -> str:
    """
    Extract user role from request.
    
    In production, this would:
    1. Verify JWT token
    2. Extract user ID
    3. Query database for user role
    
    For now, returns 'free' as default.
    """
    # TODO: Implement proper JWT verification
    # token = request.headers.get("Authorization")
    # user = verify_jwt_token(token)
    # return user.role
    
    return "free"  # Default role


def has_permission(user_role: str, required_permission: str) -> bool:
    """Check if a role has a specific permission."""
    role_data = ROLES.get(user_role)
    
    if not role_data:
        return False
    
    permissions = role_data["permissions"]
    
    # Admin has all permissions
    if "*" in permissions:
        return True
    
    return required_permission in permissions


def require_role(*allowed_roles: str):
    """
    Decorator to require specific roles.
    
    Usage:
        @require_role("premium", "admin")
        async def premium_endpoint():
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if not request:
                # Try to find request in args
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found"
                )
            
            user_role = get_user_role(request)
            
            if user_role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"This endpoint requires one of the following roles: {', '.join(allowed_roles)}"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def require_permission(required_permission: str):
    """
    Decorator to require specific permission.
    
    Usage:
        @require_permission("read:analytics")
        async def analytics_endpoint():
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if not request:
                # Try to find request in args
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
            
            if not request:
                # If no request found, allow (for testing)
                return await func(*args, **kwargs)
            
            user_role = get_user_role(request)
            
            if not has_permission(user_role, required_permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"This endpoint requires the '{required_permission}' permission"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


async def get_current_user_role(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Dependency to get current user's role from JWT token.
    
    Usage:
        async def endpoint(user_role: str = Depends(get_current_user_role)):
            ...
    """
    # Implement JWT verification and extract user role
    from src.services.auth_service import AuthService
    token = credentials.credentials
    payload = AuthService.decode_token(token)
    if payload is None:
        return "free"
    return payload.get("role", "free")


def check_rate_limit(user_role: str, current_usage: int) -> bool:
    """Check if user has exceeded rate limit."""
    role_data = ROLES.get(user_role)
    
    if not role_data:
        return False
    
    rate_limit = role_data["rate_limit"]
    
    # No limit for this role
    if rate_limit is None:
        return True
    
    return current_usage < rate_limit
