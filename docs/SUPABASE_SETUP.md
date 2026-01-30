# Supabase Setup for Vuva Project

This guide explains how to use Supabase (hosted Postgres + Storage) to host the database and file storage for Vuva.

Overview
- Use Supabase Postgres as the application `DATABASE_URL` (asyncpg prefix recommended)
- Use Supabase Storage for uploaded files (optional)

Steps

1) Create a Supabase project
- Go to https://app.supabase.com and create a new project.
- In the project dashboard copy the Postgres connection string from "Settings → Database → Connection string".

2) Configure your environment
- For async usage in the app, set `DATABASE_URL` to the asyncpg URL:

  postgresql+asyncpg://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>

- Add the URL and Supabase keys to your `.env` (example in `.env.example`):

  DATABASE_URL=postgresql+asyncpg://user:pass@db.xxx.supabase.co:5432/postgres
  SUPABASE_URL=https://<project>.supabase.co
  SUPABASE_SERVICE_ROLE_KEY=<service_role_key>

3) Install prerequisites locally (for migrations)

  - Ensure `psycopg2-binary` is installed to let Alembic run migrations against the sync DB driver that Alembic uses:

  ```bash
  pip install psycopg2-binary
  ```

4) Run database migrations

- Alembic uses `src.config.get_settings()` to obtain `DATABASE_URL` and converts the asyncpg prefix to the sync `psycopg2` prefix automatically. After exporting the environment variables, run:

  ```bash
  export DATABASE_URL='postgresql+asyncpg://user:pass@db.xxx.supabase.co:5432/postgres'
  alembic upgrade head
  ```

5) Configure file storage (optional)

- Use Supabase Storage for uploads instead of local filesystem. Options:
  - Use the `supabase` Python client (supabase-py) to upload/download files directly from the app.
  - Use the Supabase Storage REST API with the service role key for server-side uploads.

Example (using `supabase` Python client):

```python
from supabase import create_client
import os

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# upload a file to bucket 'uploads'
with open('localfile.png', 'rb') as f:
    data = f.read()
    res = supabase.storage.from_('uploads').upload('path/in/bucket/localfile.png', data)
    print(res)
```

6) App runtime

- The application can keep using `postgresql+asyncpg://` at runtime to use `asyncpg`.
- Ensure the env var is set in your deployment (CI, container, or server).

Notes & Recommendations
- Use a dedicated Supabase role/service user for the app in production. Supabase provides the connection credentials; avoid exposing the service_role key to clients.
- For Alembic, the code replaces the `asyncpg` prefix with `psycopg2` to run migrations. That's why `psycopg2-binary` is required for migration runs.
- Test migrations against a staging Supabase project before running in production.

Next Steps I can do for you
- Run `alembic upgrade head` against a Supabase connection if you provide the connection string (I can run it locally if you want).
- Add a minimal `src/services/supabase_storage.py` helper to integrate Supabase Storage into the app.
