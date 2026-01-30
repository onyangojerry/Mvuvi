import asyncio
from pathlib import Path

import pytest

from src.services.storage_service import LocalStorage


class DummyUpload:
    def __init__(self, filename: str, content: bytes, content_type: str = "image/png"):
        self.filename = filename
        self.content_type = content_type
        self._content = content

    async def read(self):
        await asyncio.sleep(0)
        return self._content


def test_local_storage_save(tmp_path):
    base = tmp_path / "uploads"
    storage = LocalStorage(base_dir=str(base))
    content = b"hello world"
    upload = DummyUpload("greeting.txt", content, "text/plain")

    result = asyncio.get_event_loop().run_until_complete(storage.save(upload))

    assert result["filename"] == "greeting.txt"
    assert result["content_type"] == "text/plain"
    assert result["size_bytes"] == len(content)
    p = Path(result["storage_path"])
    assert p.exists()
    assert p.read_bytes() == content
