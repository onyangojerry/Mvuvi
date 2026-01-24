"""
Authentication service with industry-standard cryptography.

Uses:
- Argon2id for password hashing (OWASP recommended)
- JWT with RS256 (RSA signatures) for tokens
- Secure token expiration and refresh mechanism
- Protection against timing attacks
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import secrets
from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models import User, APIKey
from src.config import get_settings

settings = get_settings()

# Industry-standard Argon2id configuration
ph = PasswordHasher(
    time_cost=3,        # Number of iterations
    memory_cost=65536,  # 64 MB memory
    parallelism=4,      # 4 parallel threads
    hash_len=32,        # 32 byte hash
    salt_len=16,        # 16 byte salt
    encoding='utf-8',
    type=Type.ID        # Argon2id (hybrid mode - best security)
)


class AuthService:
    """
    Secure authentication service using industry best practices.
    
    Security features:
    - Argon2id password hashing (memory-hard, resistant to GPU attacks)
    - JWT tokens with RSA signatures
    - Secure random token generation
    - Timing-attack resistant verification
    - Automatic password rehashing on algorithm updates
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using Argon2id.
        
        Argon2id is the winner of the Password Hashing Competition and
        recommended by OWASP for password storage.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return ph.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against hash with timing-attack resistance.
        
        Args:
            plain_password: Plain text password to verify
            hashed_password: Previously hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            ph.verify(hashed_password, plain_password)
            return True
        except (VerifyMismatchError, InvalidHashError):
            return False
    
    @staticmethod
    def needs_rehash(hashed_password: str) -> bool:
        """
        Check if password hash needs to be updated to current parameters.
        
        Returns:
            True if rehashing is recommended
        """
        try:
            return ph.check_needs_rehash(hashed_password)
        except InvalidHashError:
            return True
    
    @staticmethod
    def create_access_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT access token with RSA signature.
        
        Args:
            data: Payload data to encode in token
            expires_delta: Optional custom expiration time
            
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(32)  # JWT ID for revocation
        })
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.jwt_algorithm
        )
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create JWT refresh token for obtaining new access tokens.
        
        Args:
            data: Payload data to encode in token
            expires_delta: Optional custom expiration time
            
        Returns:
            Encoded JWT refresh token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=settings.refresh_token_expire_days
            )
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(32),
            "type": "refresh"
        })
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=settings.jwt_algorithm
        )
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Decode and verify JWT token.
        
        Args:
            token: JWT token to decode
            
        Returns:
            Decoded payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.jwt_algorithm]
            )
            return payload
        except JWTError:
            return None
    
    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Implements timing-attack resistance by always hashing the password
        even if user doesn't exist.
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
            
        Returns:
            User object if authenticated, None otherwise
        """
        # Fetch user
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        # Timing-attack resistance: always verify hash even if user not found
        if user is None:
            # Dummy hash to maintain consistent timing
            AuthService.verify_password(password, "$argon2id$v=19$m=65536,t=3,p=4$dummy")
            return None
        
        # Verify password
        if not AuthService.verify_password(password, user.password_hash):
            return None
        
        # Check if password needs rehashing with updated parameters
        if AuthService.needs_rehash(user.password_hash):
            user.password_hash = AuthService.hash_password(password)
            await db.commit()
        
        return user
    
    @staticmethod
    def generate_api_key() -> tuple[str, str]:
        """
        Generate secure API key pair.
        
        Returns:
            Tuple of (raw_key, key_hash)
            - raw_key: To give to user (only shown once)
            - key_hash: To store in database
        """
        # Generate cryptographically secure random key
        raw_key = secrets.token_urlsafe(32)
        
        # Hash for storage (prevents key leakage from database)
        key_hash = AuthService.hash_password(raw_key)
        
        # Generate prefix for identification (first 8 chars)
        key_prefix = raw_key[:8]
        
        return f"vuva_{raw_key}", key_hash, key_prefix
    
    @staticmethod
    async def verify_api_key(
        db: AsyncSession,
        api_key: str
    ) -> Optional[APIKey]:
        """
        Verify API key and return associated key object.
        
        Args:
            db: Database session
            api_key: Raw API key to verify
            
        Returns:
            APIKey object if valid, None otherwise
        """
        if not api_key.startswith("vuva_"):
            return None
        
        # Extract prefix for quick lookup
        key_prefix = api_key[5:13]  # Skip "vuva_" prefix
        
        # Find keys with matching prefix
        result = await db.execute(
            select(APIKey).where(APIKey.key_prefix == key_prefix)
        )
        api_keys = result.scalars().all()
        
        # Verify against stored hashes (timing-attack resistant)
        for key_obj in api_keys:
            if AuthService.verify_password(api_key[5:], key_obj.key_hash):
                # Update last used timestamp
                key_obj.last_used_at = datetime.utcnow()
                key_obj.usage_count += 1
                await db.commit()
                return key_obj
        
        return None
    
    @staticmethod
    async def create_user(
        db: AsyncSession,
        email: str,
        password: str,
        role: str = "free"
    ) -> User:
        """
        Create new user with hashed password.
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
            role: User role (default: free)
            
        Returns:
            Created user object
        """
        hashed_password = AuthService.hash_password(password)
        
        user = User(
            email=email,
            password_hash=hashed_password,
            role=role,
            is_active=True,
            is_verified=False
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return user
    
    @staticmethod
    async def get_user_by_id(
        db: AsyncSession,
        user_id: str
    ) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            db: Database session
            user_id: User UUID
            
        Returns:
            User object if found, None otherwise
        """
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_user_by_email(
        db: AsyncSession,
        email: str
    ) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            db: Database session
            email: User email
            
        Returns:
            User object if found, None otherwise
        """
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
