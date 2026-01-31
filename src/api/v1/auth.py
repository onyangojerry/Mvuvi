"""
Authentication API endpoints.

Provides:
- User registration with secure password hashing
- Login with JWT token generation
- Token refresh
- Password management
- API key management
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_db
from src.schemas.auth import (
    UserRegister,
    UserLogin,
    TokenResponse,
    TokenRefresh,
    UserResponse,
    PasswordChange,
    APIKeyCreate,
    APIKeyResponse
)
from src.services.auth_service import AuthService
from src.middleware.auth import require_auth, require_admin
from src.models import User, APIKey
from src.config import get_settings

settings = get_settings()
router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Register new user account with secure password hashing.
    
    Password requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    
    Uses Argon2id for password hashing (OWASP recommended).
    """
    # Check if user already exists
    existing_user = await AuthService.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user with hashed password
    user = await AuthService.create_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
        role="free"
    )
    
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return JWT tokens.
    
    Returns both access token (short-lived) and refresh token (long-lived).
    Access tokens expire in 15 minutes by default.
    Refresh tokens expire in 7 days by default.
    
    Implements timing-attack resistance.
    """
    # Authenticate user
    user = await AuthService.authenticate_user(
        db=db,
        email=credentials.email,
        password=credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token = AuthService.create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    
    refresh_token = AuthService.create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    token_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    Validates refresh token and issues new access token.
    """
    # Decode refresh token
    payload = AuthService.decode_token(token_data.refresh_token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify token type
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user
    user_id = payload.get("sub")
    user = await AuthService.get_user_by_id(db, user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create new access token
    access_token = AuthService.create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    
    # Optionally rotate refresh token (recommended for security)
    new_refresh_token = AuthService.create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user: User = Depends(require_auth)
):
    """
    Get current authenticated user information.
    
    Requires valid JWT access token.
    """
    return user


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """
    Change user password.
    
    Requires current password for verification.
    New password must meet strength requirements.
    """
    # Verify current password
    if not AuthService.verify_password(password_data.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Hash new password
    user.password_hash = AuthService.hash_password(password_data.new_password)
    
    await db.commit()
    
    return {"message": "Password changed successfully"}


@router.post("/api-keys", response_model=APIKeyResponse)
async def create_api_key(
    key_data: APIKeyCreate,
    user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """
    Create new API key for programmatic access.
    
    API key is only shown once - store it securely.
    Keys are hashed in database using Argon2id.
    """
    # Generate secure API key
    raw_key, key_hash, key_prefix = AuthService.generate_api_key()
    
    # Determine rate limit based on tier
    rate_limits = {
        "free": 100,
        "basic": 1000,
        "premium": 10000
    }
    
    # Create API key record
    api_key = APIKey(
        user_id=user.id,
        key_hash=key_hash,
        key_prefix=key_prefix,
        tier=key_data.tier,
        rate_limit=rate_limits.get(key_data.tier, 100),
        usage_count=0
    )
    
    db.add(api_key)
    await db.commit()
    await db.refresh(api_key)
    
    # Return response with raw key (only time it's shown)
    # Ensure 'name' is never None for response
    if api_key.name is None:
        api_key.name = key_data.name or "Unnamed Key"
    response = APIKeyResponse.from_orm(api_key)
    response.key = raw_key
    return response


@router.get("/api-keys", response_model=list[APIKeyResponse])
async def list_api_keys(
    user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """
    List all API keys for current user.
    
    Does not return actual key values (only shown at creation).
    """
    result = await db.execute(
        select(APIKey).where(APIKey.user_id == user.id)
    )
    api_keys = result.scalars().all()
    
    return api_keys


@router.delete("/api-keys/{key_id}")
async def delete_api_key(
    key_id: str,
    user: User = Depends(require_auth),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete API key.
    
    Users can only delete their own keys.
    """
    result = await db.execute(
        select(APIKey).where(
            APIKey.id == key_id,
            APIKey.user_id == user.id
        )
    )
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    await db.delete(api_key)
    await db.commit()
    
    return {"message": "API key deleted successfully"}
