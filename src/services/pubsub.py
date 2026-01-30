"""Redis pub/sub helper utilities."""
import json
import asyncio
from typing import Any
import redis.asyncio as aioredis

from src.config import get_settings

settings = get_settings()


async def publish_event(channel: str, payload: Any) -> None:
    """Publish a JSON payload to Redis channel (async)."""
    try:
        r = aioredis.from_url(settings.redis_url)
        await r.publish(channel, json.dumps(payload))
    except Exception:
        # Best-effort publish; swallowing errors so web request isn't blocked
        pass
