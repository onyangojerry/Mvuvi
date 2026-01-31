# File Storage Implementation (Backend)

## Organization
- All uploaded files are stored under `uploads/{user_id}/{YYYY-MM-DD}/` for easy management and cleanup.
- Anonymous uploads are stored under `uploads/anonymous/{YYYY-MM-DD}/`.

## Retention Policy
- Files older than 30 days are automatically deleted by the `cleanup_old_files` method in `LocalStorage`.
- Admins can trigger cleanup via the `/api/v1/ingest/cleanup-uploads` endpoint.

## Upload Flow
- Upload endpoints (`/api/v1/ingest/upload`) save files using the user's ID (if available) for organized storage.
- File metadata (filename, content type, size, storage path) is tracked in the database via the `OCRJob` model.

## Download/Access
- (Planned) Add secure download endpoint for users to access their uploaded files.

## Cloud Storage
- (Planned) Add S3/Supabase storage option for production deployments.

## Configuration
- Storage directory and retention period are configurable in `src/config.py`.

## Example Usage
```python
from src.services.storage_service import get_storage
storage = get_storage()
# Save file
await storage.save(upload_file, user_id="user-uuid")
# Cleanup old files
storage.cleanup_old_files()
```

---
*Last updated: January 30, 2026*