"""
Initial database schema migration.

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-01-24

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema."""
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False, server_default='free'),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('is_verified', sa.Boolean(), server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('idx_user_email', 'users', ['email'])
    op.create_index('idx_user_role', 'users', ['role'])
    
    # Create sources table
    op.create_table(
        'sources',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('feed_type', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('language', sa.String(10), server_default='en'),
        sa.Column('country', sa.String(10), nullable=True),
        sa.Column('article_count', sa.Integer(), server_default='0'),
        sa.Column('last_fetched_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )
    op.create_index('idx_source_category', 'sources', ['category'])
    op.create_index('idx_source_active', 'sources', ['is_active'])
    
    # Create articles table
    op.create_table(
        'articles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('sources.id'), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('url', sa.Text(), unique=True, nullable=False),
        sa.Column('author', sa.String(255), nullable=True),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('image_url', sa.Text(), nullable=True),
        sa.Column('is_extracted', sa.Boolean(), server_default='false'),
        sa.Column('extraction_status', sa.String(50), server_default='pending'),
        sa.Column('view_count', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )
    op.create_index('idx_article_source', 'articles', ['source_id'])
    op.create_index('idx_article_published', 'articles', ['published_at'])
    op.create_index('idx_article_created', 'articles', ['created_at'])
    
    # Create api_keys table
    op.create_table(
        'api_keys',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('key_hash', sa.String(255), unique=True, nullable=False),
        sa.Column('key_prefix', sa.String(20), nullable=False),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('tier', sa.String(50), nullable=False, server_default='free'),
        sa.Column('rate_limit', sa.Integer(), nullable=False, server_default='100'),
        sa.Column('usage_count', sa.Integer(), server_default='0'),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default='true'),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )
    op.create_index('idx_apikey_user', 'api_keys', ['user_id'])
    op.create_index('idx_apikey_hash', 'api_keys', ['key_hash'])
    
    # Create user_preferences table
    op.create_table(
        'user_preferences',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), unique=True, nullable=False),
        sa.Column('favorite_categories', sa.Text(), nullable=True),
        sa.Column('preferred_sources', sa.Text(), nullable=True),
        sa.Column('language', sa.String(10), server_default='en'),
        sa.Column('email_notifications', sa.Boolean(), server_default='true'),
        sa.Column('news_digest_frequency', sa.String(20), server_default='daily'),
        sa.Column('articles_per_page', sa.Integer(), server_default='20'),
        sa.Column('default_view', sa.String(20), server_default='list'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )
    
    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('event_type', sa.String(100), nullable=False),
        sa.Column('action', sa.String(255), nullable=False),
        sa.Column('resource', sa.String(255), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('api_key_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('request_id', sa.String(100), nullable=True),
        sa.Column('status_code', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('metadata', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index('idx_audit_user', 'audit_logs', ['user_id'])
    op.create_index('idx_audit_event', 'audit_logs', ['event_type'])
    op.create_index('idx_audit_created', 'audit_logs', ['created_at'])
    
    # Create ocr_jobs table
    op.create_table(
        'ocr_jobs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('engine', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('extracted_text', sa.Text(), nullable=True),
        sa.Column('confidence', sa.Integer(), nullable=True),
        sa.Column('word_count', sa.Integer(), nullable=True),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.Column('file_size_kb', sa.Integer(), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('idx_ocr_user', 'ocr_jobs', ['user_id'])
    op.create_index('idx_ocr_status', 'ocr_jobs', ['status'])
    op.create_index('idx_ocr_created', 'ocr_jobs', ['created_at'])


def downgrade() -> None:
    """Drop all tables."""
    op.drop_table('ocr_jobs')
    op.drop_table('audit_logs')
    op.drop_table('user_preferences')
    op.drop_table('api_keys')
    op.drop_table('articles')
    op.drop_table('sources')
    op.drop_table('users')
