import os
from pathlib import Path
from typing import Dict
from uuid import uuid4

from fastapi import UploadFile

from src.config import get_settings

settings = get_settings()


import shutil
from datetime import datetime, timedelta

class LocalStorage:
    def __init__(self, base_dir: str = "./uploads", retention_days: int = 30):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.retention_days = retention_days

    async def save(self, upload: UploadFile, user_id: str = None) -> Dict[str, str]:
        ext = Path(upload.filename).suffix
        today = datetime.utcnow().strftime("%Y-%m-%d")
        user_folder = user_id if user_id else "anonymous"
        target_dir = self.base_dir / user_folder / today
        target_dir.mkdir(parents=True, exist_ok=True)
        fname = f"{uuid4()}{ext}"
        target = target_dir / fname
        contents = await upload.read()
        target.write_bytes(contents)
        return {
            "filename": upload.filename,
            "storage_path": str(target),
            "content_type": upload.content_type,
            "size_bytes": len(contents),
        }

    def cleanup_old_files(self):
        """Remove files older than retention_days from storage."""
        cutoff = datetime.utcnow() - timedelta(days=self.retention_days)
        for user_dir in self.base_dir.iterdir():
            if not user_dir.is_dir():
                continue
            for date_dir in user_dir.iterdir():
                if not date_dir.is_dir():
                    continue
                try:
                    dir_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
                except Exception:
                    continue
                if dir_date < cutoff:
                    shutil.rmtree(date_dir)


def get_storage():
    # For now return local storage; in production this factory can return S3/Supabase storage
    return LocalStorage(settings.upload_dir)
