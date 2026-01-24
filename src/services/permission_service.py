"""Permission service for RBAC."""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models import User, APIKey


class PermissionService:
    """Service for managing permissions and roles."""
    
    @staticmethod
    async def get_user_permissions(user_id: str, db: AsyncSession) -> List[str]:
        """Get all permissions for a user based on their role."""
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return []
        
        # Import here to avoid circular dependency
        from src.middleware.authorization import ROLES
        
        role_data = ROLES.get(user.role, {})
        return role_data.get("permissions", [])
    
    @staticmethod
    async def has_permission(
        user_id: str,
        permission: str,
        db: AsyncSession
    ) -> bool:
        """Check if user has a specific permission."""
        permissions = await PermissionService.get_user_permissions(user_id, db)
        
        # Admin has all permissions
        if "*" in permissions:
            return True
        
        return permission in permissions
    
    @staticmethod
    async def get_user_rate_limit(user_id: str, db: AsyncSession) -> Optional[int]:
        """Get rate limit for a user based on their role."""
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return 100  # Default free tier limit
        
        from src.middleware.authorization import ROLES
        
        role_data = ROLES.get(user.role, {})
        return role_data.get("rate_limit", 100)
    
    @staticmethod
    async def check_api_key_permissions(
        api_key_hash: str,
        permission: str,
        db: AsyncSession
    ) -> bool:
        """Check if an API key has a specific permission."""
        result = await db.execute(
            select(APIKey).where(APIKey.key_hash == api_key_hash)
        )
        api_key = result.scalar_one_or_none()
        
        if not api_key or not api_key.is_active:
            return False
        
        # Get user permissions
        return await PermissionService.has_permission(
            str(api_key.user_id),
            permission,
            db
        )
    
    @staticmethod
    async def upgrade_user_role(
        user_id: str,
        new_role: str,
        db: AsyncSession
    ) -> bool:
        """Upgrade a user's role (admin only)."""
        valid_roles = ["free", "basic", "premium", "admin"]
        
        if new_role not in valid_roles:
            return False
        
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return False
        
        user.role = new_role
        await db.commit()
        return True
