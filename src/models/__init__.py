"""
SQLAlchemy database models for Vuva.
"""

from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import Column, String, Boolean, Integer, DateTime, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    """User model for authentication and authorization."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="free")  # free, basic, premium, admin
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_user_email', 'email'),
        Index('idx_user_role', 'role'),
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"


class Source(Base):
    """News source model."""
    
    __tablename__ = "sources"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)  # technology, world, business, science, general
    feed_type = Column(String(50), nullable=False)  # rss, api, scrape
    is_active = Column(Boolean, default=True)
    
    # Metadata
    description = Column(Text, nullable=True)
    language = Column(String(10), default="en")
    country = Column(String(10), nullable=True)
    
    # Stats
    article_count = Column(Integer, default=0)
    last_fetched_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    articles = relationship("Article", back_populates="source", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index('idx_source_category', 'category'),
        Index('idx_source_active', 'is_active'),
    )
    
    def __repr__(self):
        return f"<Source(id={self.id}, name={self.name}, category={self.category})>"


class Article(Base):
    """News article model."""
    
    __tablename__ = "articles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)
    
    # Content
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=True)  # Full article content
    summary = Column(Text, nullable=True)
    url = Column(Text, unique=True, nullable=False)
    
    # Metadata
    author = Column(String(255), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    image_url = Column(Text, nullable=True)
    
    # Processing
    is_extracted = Column(Boolean, default=False)  # Whether full content is extracted
    extraction_status = Column(String(50), default="pending")  # pending, success, failed
    
    # Stats
    view_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    source = relationship("Source", back_populates="articles")
    
    # Indexes
    __table_args__ = (
        Index('idx_article_source', 'source_id'),
        Index('idx_article_published', 'published_at'),
        Index('idx_article_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Article(id={self.id}, title={self.title[:50]})>"


class APIKey(Base):
    """API key model for authentication."""
    
    __tablename__ = "api_keys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Key details
    key_hash = Column(String(255), unique=True, nullable=False, index=True)
    key_prefix = Column(String(20), nullable=False)  # vuva_xxxxx (for display)
    name = Column(String(255), nullable=True)  # User-friendly name
    
    # Tier and limits
    tier = Column(String(50), nullable=False, default="free")  # free, basic, premium
    rate_limit = Column(Integer, nullable=False, default=100)  # requests per hour
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    
    # Lifecycle
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
    # Indexes
    __table_args__ = (
        Index('idx_apikey_user', 'user_id'),
        Index('idx_apikey_hash', 'key_hash'),
    )
    
    def __repr__(self):
        return f"<APIKey(id={self.id}, prefix={self.key_prefix}, tier={self.tier})>"


class UserPreference(Base):
    """User preferences and settings."""
    
    __tablename__ = "user_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)
    
    # Preferences
    favorite_categories = Column(Text, nullable=True)  # JSON array
    preferred_sources = Column(Text, nullable=True)  # JSON array
    language = Column(String(10), default="en")
    
    # Notification settings
    email_notifications = Column(Boolean, default=True)
    news_digest_frequency = Column(String(20), default="daily")  # never, daily, weekly
    
    # Display settings
    articles_per_page = Column(Integer, default=20)
    default_view = Column(String(20), default="list")  # list, grid, compact
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="preferences")
    
    def __repr__(self):
        return f"<UserPreference(user_id={self.user_id})>"


class AuditLog(Base):
    """Audit log for security and compliance."""
    
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Event details
    event_type = Column(String(100), nullable=False)  # login, logout, api_call, etc.
    action = Column(String(255), nullable=False)
    resource = Column(String(255), nullable=True)
    
    # User context
    user_id = Column(UUID(as_uuid=True), nullable=True)
    api_key_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Request context
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    request_id = Column(String(100), nullable=True)
    
    # Response
    status_code = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Additional data
    extra_data = Column(Text, nullable=True)  # JSON - renamed from metadata
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Indexes
    __table_args__ = (
        Index('idx_audit_user', 'user_id'),
        Index('idx_audit_event', 'event_type'),
        Index('idx_audit_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, event={self.event_type}, action={self.action})>"


class OCRJob(Base):
    """OCR processing job tracking."""
    
    __tablename__ = "ocr_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Job details
    filename = Column(String(255), nullable=False)
    engine = Column(String(50), nullable=False)  # tesseract, easyocr, paddleocr
    status = Column(String(50), nullable=False, default="pending")  # pending, processing, completed, failed
    
    # Results
    extracted_text = Column(Text, nullable=True)
    confidence = Column(Integer, nullable=True)
    word_count = Column(Integer, nullable=True)
    
    # Performance
    processing_time_ms = Column(Integer, nullable=True)
    file_size_kb = Column(Integer, nullable=True)
    
    # Error handling
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_ocr_user', 'user_id'),
        Index('idx_ocr_status', 'status'),
        Index('idx_ocr_created', 'created_at'),
    )
    
    def __repr__(self):
        return f"<OCRJob(id={self.id}, filename={self.filename}, status={self.status})>"
