"""
Authentication middleware with JWT token verification.

Provides:
- JWT token extraction and verification
- User authentication dependency
- Optional authentication (for public/private endpoints)
- Token refresh handling
"""

from typing import Optional
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.services.auth_service import AuthService
from src.models import User

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer token
        db: Database session
        
    Returns:
        User object if authenticated, None otherwise
    """
    if credentials is None:
        return None
    
    token = credentials.credentials
    
    # Decode token
    payload = AuthService.decode_token(token)
    if payload is None:
        return None
    
    # Extract user ID
    user_id = payload.get("sub")
    if user_id is None:
        return None
    
    # Verify token type
    token_type = payload.get("type", "access")
    if token_type != "access":
        return None
    
    # Get user from database
    user = await AuthService.get_user_by_id(db, user_id)
    if user is None:
        return None
    
    # Check if user is active
    if not user.is_active:
        return None
    
    return user


async def require_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Require authentication - raises exception if not authenticated.
    
    Args:
        credentials: HTTP Bearer token
        db: Database session
        
    Returns:
        Authenticated user object
        
    Raises:
        HTTPException: If not authenticated or token invalid
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await get_current_user(credentials, db)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def require_verified_user(
    user: User = Depends(require_auth)
) -> User:
    """
    Require verified user account.
    
    Args:
        user: Authenticated user
        
    Returns:
        Verified user object
        
    Raises:
        HTTPException: If user email not verified
    """
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required"
        )
    
    return user


async def require_admin(
    user: User = Depends(require_auth)
) -> User:
    """
    Require admin role.
    
    Args:
        user: Authenticated user
        
    Returns:
        Admin user object
        
    Raises:
        HTTPException: If user is not admin
    """
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return user


def get_optional_user(
    user: Optional[User] = Depends(get_current_user)
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise.
    Useful for endpoints that work both with and without authentication.
    
    Args:
        user: Optional authenticated user
        
    Returns:
        User object if authenticated, None otherwise
    """
    return user
