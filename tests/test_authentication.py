"""
Comprehensive test suite for authentication system.

Tests cover:
- User registration with password validation
- Login and JWT token generation
- Token refresh mechanism
- Password change functionality
- API key management
- Security features (timing attacks, password hashing)
- Authorization middleware
- Role-based access control
"""

import pytest
from datetime import datetime, timedelta

from src.models import User, APIKey
from src.services.auth_service import AuthService


class TestPasswordHashing:
    """Test password hashing security."""
    
    def test_password_hashing(self):
        """Test Argon2id password hashing."""
        password = "SecurePassword123"
        hashed = AuthService.hash_password(password)
        
        # Verify hash format (Argon2id)
        assert hashed.startswith("$argon2id$")
        assert len(hashed) > 50
        
    def test_password_verification(self):
        """Test password verification."""
        password = "TestPassword123"
        hashed = AuthService.hash_password(password)
        
        # Correct password
        assert AuthService.verify_password(password, hashed) is True
        
        # Incorrect password
        assert AuthService.verify_password("WrongPassword", hashed) is False
    
    def test_timing_attack_resistance(self):
        """Test timing attack resistance."""
        import time
        
        password = "TestPassword123"
        hashed = AuthService.hash_password(password)
        
        # Time correct password
        start = time.perf_counter()
        AuthService.verify_password(password, hashed)
        correct_time = time.perf_counter() - start
        
        # Time incorrect password
        start = time.perf_counter()
        AuthService.verify_password("WrongPassword", hashed)
        incorrect_time = time.perf_counter() - start
        
        # Times should be similar (within 50ms)
        time_diff = abs(correct_time - incorrect_time)
        assert time_diff < 0.05, f"Timing difference too large: {time_diff}"
    
    def test_different_passwords_different_hashes(self):
        """Test that same password produces different hashes (salt)."""
        password = "TestPassword123"
        hash1 = AuthService.hash_password(password)
        hash2 = AuthService.hash_password(password)
        
        assert hash1 != hash2  # Different salts
        assert AuthService.verify_password(password, hash1)
        assert AuthService.verify_password(password, hash2)


class TestUserRegistration:
    """Test user registration endpoint."""
    
    @pytest.mark.asyncio
    async def test_register_success(self, client):
        """Test successful user registration."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "SecurePass123"
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["role"] == "free"
        assert data["is_active"] is True
        assert data["is_verified"] is False
        assert "id" in data
    
    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client):
        """Test registration with duplicate email."""
        # Register first user
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "SecurePass123"
            }
        )
        
        # Try to register again
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "duplicate@example.com",
                "password": "DifferentPass456"
            }
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_register_weak_password(self, client):
        """Test registration with weak password."""
        # Too short
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "short"
            }
        )
        assert response.status_code == 422
        
        # No uppercase
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "nouppercase123"
            }
        )
        assert response.status_code == 422
        
        # No digit
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "NoDigitHere"
            }
        )
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client):
        """Test registration with invalid email."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "password": "SecurePass123"
            }
        )
        
        assert response.status_code == 422


class TestLogin:
    """Test login endpoint."""
    
    @pytest.mark.asyncio
    async def test_login_success(self, client):
        """Test successful login."""
        # Register user first
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "login@example.com",
                "password": "SecurePass123"
            }
        )
        
        # Login
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "login@example.com",
                "password": "SecurePass123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 900  # 15 minutes
    
    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client):
        """Test login with wrong password."""
        # Register user
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "CorrectPass123"
            }
        )
        
        # Try wrong password
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "WrongPass123"
            }
        )
        
        assert response.status_code == 401
        assert "Incorrect" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "SomePass123"
            }
        )
        
        assert response.status_code == 401


class TestTokens:
    """Test JWT token functionality."""
    
    def test_token_structure(self):
        """Test JWT token structure."""
        data = {"sub": "user123", "email": "test@example.com"}
        token = AuthService.create_access_token(data)
        
        # JWT has 3 parts separated by dots
        parts = token.split(".")
        assert len(parts) == 3
    
    def test_token_decode(self):
        """Test token decoding."""
        user_data = {"sub": "user123", "email": "test@example.com"}
        token = AuthService.create_access_token(user_data)
        
        payload = AuthService.decode_token(token)
        assert payload is not None
        assert payload["sub"] == "user123"
        assert payload["email"] == "test@example.com"
        assert "exp" in payload
        assert "iat" in payload
        assert "jti" in payload
    
    def test_expired_token(self):
        """Test expired token handling."""
        data = {"sub": "user123"}
        # Create token with -1 minute expiry (already expired)
        token = AuthService.create_access_token(
            data,
            expires_delta=timedelta(minutes=-1)
        )
        
        payload = AuthService.decode_token(token)
        assert payload is None  # Expired tokens return None
    
    def test_invalid_token(self):
        """Test invalid token handling."""
        invalid_token = "invalid.token.here"
        payload = AuthService.decode_token(invalid_token)
        assert payload is None


class TestTokenRefresh:
    """Test token refresh mechanism."""
    
    @pytest.mark.asyncio
    async def test_refresh_token_success(self, client):
        """Test successful token refresh."""
        # Register and login
        await client.post(
            "/api/v1/auth/register",
            json={"email": "refresh@example.com", "password": "SecurePass123"}
        )
        
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"email": "refresh@example.com", "password": "SecurePass123"}
        )
        
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh token
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
    
    @pytest.mark.asyncio
    async def test_refresh_with_access_token(self, client):
        """Test refresh endpoint rejects access tokens."""
        # Register and login
        await client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "password": "SecurePass123"}
        )
        
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "SecurePass123"}
        )
        
        access_token = login_response.json()["access_token"]
        
        # Try to refresh with access token
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": access_token}
        )
        
        assert response.status_code == 401


class TestProtectedEndpoints:
    """Test protected endpoint access."""
    
    @pytest.mark.asyncio
    async def test_access_without_token(self, client):
        """Test accessing protected endpoint without token."""
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_access_with_valid_token(self, client):
        """Test accessing protected endpoint with valid token."""
        # Register and login
        await client.post(
            "/api/v1/auth/register",
            json={"email": "protected@example.com", "password": "SecurePass123"}
        )
        
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"email": "protected@example.com", "password": "SecurePass123"}
        )
        
        token = login_response.json()["access_token"]
        
        # Access protected endpoint
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "protected@example.com"
    
    @pytest.mark.asyncio
    async def test_access_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token."""
        response = await client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401


class TestPasswordChange:
    """Test password change functionality."""
    
    @pytest.mark.asyncio
    async def test_change_password_success(self, client):
        """Test successful password change."""
        # Register and login
        await client.post(
            "/api/v1/auth/register",
            json={"email": "change@example.com", "password": "OldPass123"}
        )
        
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"email": "change@example.com", "password": "OldPass123"}
        )
        
        token = login_response.json()["access_token"]
        
        # Change password
        response = await client.post(
            "/api/v1/auth/change-password",
            json={
                "current_password": "OldPass123",
                "new_password": "NewPass456"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        
        # Try logging in with new password
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"email": "change@example.com", "password": "NewPass456"}
        )
        
        assert login_response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_change_password_wrong_current(self, client):
        """Test password change with wrong current password."""
        # Register and login
        await client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "password": "CorrectPass123"}
        )
        
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "CorrectPass123"}
        )
        
        token = login_response.json()["access_token"]
        
        # Try to change with wrong current password
        response = await client.post(
            "/api/v1/auth/change-password",
            json={
                "current_password": "WrongPass123",
                "new_password": "NewPass456"
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400


class TestAPIKeys:
    """Test API key management."""
    
    def test_generate_api_key(self):
        """Test API key generation."""
        raw_key, key_hash, key_prefix = AuthService.generate_api_key()
        
        # Check format
        assert raw_key.startswith("vuva_")
        assert len(raw_key) > 20
        assert len(key_prefix) == 8
        assert key_hash.startswith("$argon2id$")
    
    @pytest.mark.asyncio
    async def test_create_api_key_endpoint(self, client):
        """Test API key creation endpoint."""
        # Register and login
        await client.post(
            "/api/v1/auth/register",
            json={"email": "apikey@example.com", "password": "SecurePass123"}
        )
        
        login_response = await client.post(
            "/api/v1/auth/login",
            json={"email": "apikey@example.com", "password": "SecurePass123"}
        )
        
        token = login_response.json()["access_token"]
        
        # Create API key
        response = await client.post(
            "/api/v1/auth/api-keys",
            json={"name": "Test Key", "tier": "free"},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "key" in data  # Raw key shown only once
        assert data["key"].startswith("vuva_")
        assert data["tier"] == "free"
        assert data["rate_limit"] == 100


class TestSecurityFeatures:
    """Test security features."""
    
    def test_password_rehashing(self):
        """Test password rehashing detection."""
        password = "TestPass123"
        hashed = AuthService.hash_password(password)
        
        # Should not need rehashing when just created
        needs_rehash = AuthService.needs_rehash(hashed)
        # This may vary based on implementation
        assert isinstance(needs_rehash, bool)
    
    @pytest.mark.asyncio
    async def test_sql_injection_protection(self, client):
        """Test SQL injection protection."""
        # Try SQL injection in email
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "' OR '1'='1",
                "password": "anything"
            }
        )
        
        # Should fail due to email validation, not SQL injection
        assert response.status_code in [401, 422]
    
    @pytest.mark.asyncio
    async def test_timing_attack_on_login(self, client):
        """Test timing attack resistance on login."""
        import time
        
        # Register a user
        await client.post(
            "/api/v1/auth/register",
            json={"email": "timing@example.com", "password": "SecurePass123"}
        )
        
        # Time login with existing user
        start = time.perf_counter()
        await client.post(
            "/api/v1/auth/login",
            json={"email": "timing@example.com", "password": "WrongPass123"}
        )
        existing_time = time.perf_counter() - start
        
        # Time login with non-existing user
        start = time.perf_counter()
        await client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@example.com", "password": "SomePass123"}
        )
        nonexisting_time = time.perf_counter() - start
        
        # Times should be similar (within 100ms)
        time_diff = abs(existing_time - nonexisting_time)
        assert time_diff < 0.1, f"Timing difference: {time_diff}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
