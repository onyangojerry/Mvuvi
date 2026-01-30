"""Main FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.api.v1 import router as v1_router
from src.middleware.logging import LoggingMiddleware
from src.monitoring.metrics import metrics_middleware, get_metrics
from src.utils.logger import setup_logging
from src.database import init_db, check_db_connection
from src.ws.redis_ws import start_redis_subscriber, ws_manager
import asyncio

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan events."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(f"Environment: {settings.environment}")
    print(f"Debug mode: {settings.debug}")
    
    # Setup structured logging
    setup_logging(level=settings.log_level if hasattr(settings, 'log_level') else "INFO")
    print("[OK] Structured logging configured")
    
    # Initialize database (if configured)
    try:
        if settings.database_url and not settings.database_url.endswith("/postgres"):
            await init_db()
            db_healthy = await check_db_connection()
            if db_healthy:
                print("[OK] Database connection established")
            else:
                print("[WARN] Database connection failed (optional for current features)")
        else:
            print("[INFO] Database not configured (optional for current features)")
    except Exception as e:
        print(f"[WARN] Database initialization failed: {e}")
        print("  Application will run without database features")

    # Start Redis subscriber for WebSocket broadcasts
    try:
        app.state.redis_subscriber_task = asyncio.create_task(
            start_redis_subscriber(app, settings.redis_url, settings.redis_notifications_channel)
        )
        print("[OK] Redis websocket subscriber started")
    except Exception as e:
        print(f"[WARN] Redis websocket subscriber failed to start: {e}")
    
    yield
    # Shutdown
    # Cancel Redis subscriber if running
    sub_task = getattr(app.state, "redis_subscriber_task", None)
    if sub_task:
        sub_task.cancel()
        try:
            await sub_task
        except Exception:
            pass
    print("Shutting down application")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Lightweight API for newspaper ingestion with OCR, AI processing, and personalized news feeds",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)


# Middleware - ORDER MATTERS!
# 1. Logging middleware (first to capture all requests)
app.add_middleware(LoggingMiddleware)

# 2. CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. GZip middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 4. Metrics middleware
app.middleware("http")(metrics_middleware)


# Include API routers
app.include_router(v1_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "operational",
        "environment": settings.environment,
        "docs_url": "/docs" if settings.debug else None,
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "version": settings.app_version,
    }


@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """Prometheus metrics endpoint."""
    return await get_metrics()


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred",
                "details": str(exc) if settings.debug else None,
            },
        },
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
