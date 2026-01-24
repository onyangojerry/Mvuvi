"""Application configuration using Pydantic settings."""

from functools import lru_cache
from typing import List

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = Field(default="Newspaper Ingestion API")
    app_version: str = Field(default="1.0.0")
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)

    # Security
    secret_key: str = Field(default="insecure-secret-key-change-me")
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=15)
    refresh_token_expire_days: int = Field(default=7)

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:password@localhost:5432/newspaper_db"
    )

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")
    redis_max_connections: int = Field(default=50)
    
    # Cache TTL Settings (in seconds)
    cache_ocr_ttl: int = Field(default=3600)  # 1 hour
    cache_articles_ttl: int = Field(default=300)  # 5 minutes
    cache_preferences_ttl: int = Field(default=900)  # 15 minutes
    cache_enabled: bool = Field(default=True)

    # Rate Limiting
    rate_limit_free_tier: int = Field(default=100)
    rate_limit_basic_tier: int = Field(default=1000)
    rate_limit_premium_tier: int = Field(default=10000)

    # OCR Settings
    ocr_engine: str = Field(default="tesseract")
    ocr_languages: str = Field(default="eng")
    ocr_timeout_seconds: int = Field(default=30)
    max_image_size_mb: int = Field(default=10)

    # File Storage
    upload_dir: str = Field(default="./uploads")
    max_upload_size: int = Field(default=10485760)  # 10MB

    # News Sources
    news_api_enabled: bool = Field(default=True)
    rss_feeds_enabled: bool = Field(default=True)

    # Logging
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")

    # CORS
    allowed_origins: str = Field(default="http://localhost:3000,http://localhost:8000")

    @validator("allowed_origins")
    def parse_origins(cls, v: str) -> List[str]:
        """Parse comma-separated origins into a list."""
        return [origin.strip() for origin in v.split(",")]

    @property
    def max_upload_size_bytes(self) -> int:
        """Convert MB to bytes for upload size limit."""
        return self.max_image_size_mb * 1024 * 1024

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
