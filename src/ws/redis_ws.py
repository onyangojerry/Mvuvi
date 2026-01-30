"""WebSocket manager that subscribes to Redis notifications and broadcasts to clients."""
import asyncio
import json
from typing import Set

import redis.asyncio as aioredis
from fastapi import WebSocket

from src.config import get_settings

settings = get_settings()


class WebSocketManager:
    def __init__(self):
        self._connections: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self._connections.add(ws)

    async def disconnect(self, ws: WebSocket):
        self._connections.discard(ws)

    async def broadcast(self, message: dict):
        data = json.dumps(message)
        coros = [conn.send_text(data) for conn in list(self._connections)]
        if coros:
            await asyncio.gather(*coros, return_exceptions=True)


ws_manager = WebSocketManager()


async def start_redis_subscriber(app, redis_url: str, channel: str):
    """Background task: subscribe to Redis channel and forward to websockets."""
    r = aioredis.from_url(redis_url)
    pubsub = r.pubsub()
    await pubsub.subscribe(channel)
    try:
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message:
                # message dictionary: {'type': 'message', 'pattern': None, 'channel': b'chan', 'data': b'...'}
                try:
                    data = message.get("data")
                    if isinstance(data, (bytes, bytearray)):
                        text = data.decode("utf-8")
                        payload = json.loads(text)
                    else:
                        payload = data
                except Exception:
                    payload = {"event": "invalid_message", "raw": str(data)}
                await ws_manager.broadcast(payload)
            await asyncio.sleep(0.01)
    except asyncio.CancelledError:
        await pubsub.unsubscribe(channel)
    finally:
        await pubsub.close()
