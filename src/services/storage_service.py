import os
from pathlib import Path
from typing import Dict
from uuid import uuid4

from fastapi import UploadFile

from src.config import get_settings

settings = get_settings()


class LocalStorage:
    def __init__(self, base_dir: str = "./uploads"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, upload: UploadFile) -> Dict[str, str]:
        ext = Path(upload.filename).suffix
        fname = f"{uuid4()}{ext}"
        target = self.base_dir / fname
        contents = await upload.read()
        target.write_bytes(contents)
        return {
            "filename": upload.filename,
            "storage_path": str(target),
            "content_type": upload.content_type,
            "size_bytes": len(contents),
        }


def get_storage():
    # For now return local storage; in production this factory can return S3/Supabase storage
    return LocalStorage(settings.upload_dir)
