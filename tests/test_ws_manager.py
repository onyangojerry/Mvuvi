import asyncio

import pytest

from src.ws.redis_ws import ws_manager


class DummyConn:
    def __init__(self):
        self.sent = None

    async def send_text(self, data: str):
        self.sent = data


@pytest.mark.asyncio
async def test_ws_manager_broadcast():
    dummy = DummyConn()
    # insert into internal connections set
    ws_manager._connections.add(dummy)
    await ws_manager.broadcast({"hello": "world"})
    assert dummy.sent is not None
    assert "hello" in dummy.sent
    ws_manager._connections.discard(dummy)
