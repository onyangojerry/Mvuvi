"""
Structured logging configuration for Vuva.
"""

import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict
from pathlib import Path

import structlog
from structlog.stdlib import LoggerFactory


# Create logs directory
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add extra fields
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


def setup_logging(level: str = "INFO", log_file: str = "app.log"):
    """
    Configure structured logging.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Log file name in logs/ directory
    """
    
    # Convert string level to logging constant
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        handlers=[
            # Console handler (human-readable)
            logging.StreamHandler(sys.stdout),
            # File handler (JSON)
            logging.FileHandler(LOGS_DIR / log_file)
        ]
    )
    
    # Get root logger
    root_logger = logging.getLogger()
    
    # Add JSON formatter to file handler
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.setFormatter(JSONFormatter())
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger()


class RequestLogger:
    """Logger for HTTP requests."""
    
    def __init__(self):
        self.logger = structlog.get_logger("vuva.requests")
    
    def log_request(
        self,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        request_id: str = None,
        user_id: str = None,
        ip_address: str = None
    ):
        """Log an HTTP request."""
        self.logger.info(
            "http_request",
            method=method,
            path=path,
            status_code=status_code,
            duration_ms=duration_ms,
            request_id=request_id,
            user_id=user_id,
            ip_address=ip_address
        )
    
    def log_error(
        self,
        method: str,
        path: str,
        error: str,
        request_id: str = None,
        user_id: str = None
    ):
        """Log an error."""
        self.logger.error(
            "http_error",
            method=method,
            path=path,
            error=error,
            request_id=request_id,
            user_id=user_id
        )


class OCRLogger:
    """Logger for OCR operations."""
    
    def __init__(self):
        self.logger = structlog.get_logger("vuva.ocr")
    
    def log_processing(
        self,
        engine: str,
        filename: str,
        duration_ms: float,
        word_count: int,
        confidence: int,
        user_id: str = None
    ):
        """Log OCR processing."""
        self.logger.info(
            "ocr_processing",
            engine=engine,
            filename=filename,
            duration_ms=duration_ms,
            word_count=word_count,
            confidence=confidence,
            user_id=user_id
        )
    
    def log_error(
        self,
        engine: str,
        filename: str,
        error: str,
        user_id: str = None
    ):
        """Log OCR error."""
        self.logger.error(
            "ocr_error",
            engine=engine,
            filename=filename,
            error=error,
            user_id=user_id
        )


class AuditLogger:
    """Logger for security audit events."""
    
    def __init__(self):
        self.logger = structlog.get_logger("vuva.audit")
    
    def log_event(
        self,
        event_type: str,
        action: str,
        user_id: str = None,
        resource: str = None,
        ip_address: str = None,
        metadata: Dict[str, Any] = None
    ):
        """Log an audit event."""
        self.logger.info(
            "audit_event",
            event_type=event_type,
            action=action,
            user_id=user_id,
            resource=resource,
            ip_address=ip_address,
            metadata=metadata or {}
        )
    
    def log_security_event(
        self,
        event_type: str,
        severity: str,
        description: str,
        user_id: str = None,
        ip_address: str = None
    ):
        """Log a security event."""
        self.logger.warning(
            "security_event",
            event_type=event_type,
            severity=severity,
            description=description,
            user_id=user_id,
            ip_address=ip_address
        )


# Global logger instances
request_logger = RequestLogger()
ocr_logger = OCRLogger()
audit_logger = AuditLogger()


def get_logger(name: str):
    """Get a logger instance."""
    return structlog.get_logger(name)
