#!/usr/bin/env bash
set -euo pipefail

# Initialize local Postgres DB for Vuva (assumes Homebrew Postgres or docker-based Postgres available)

DB_URL=${DB_URL:-}
PSQL=${PSQL:-/opt/homebrew/opt/postgresql@15/bin/psql}

echo "Applying local schema to database..."
# If DB_URL provided, use it; otherwise try socket auth with current user (psql -d newspaper_db)
if [ -n "$DB_URL" ]; then
	${PSQL} "$DB_URL" -f db/ddl/vuva_local_schema.sql
else
	${PSQL} -d newspaper_db -f db/ddl/vuva_local_schema.sql
fi

echo "Seeding admin user (generate ARGON2 hash and set ADMIN_PASSWORD env to use custom password)..."
ADMIN_PASSWORD=${ADMIN_PASSWORD:-AdminPass123!}
ARGON2_HASH=$(python3 - <<'PY'
from argon2 import PasswordHasher
ph=PasswordHasher()
print(ph.hash('${ADMIN_PASSWORD}'))
PY
)

if [ -n "$DB_URL" ]; then
	${PSQL} "$DB_URL" -c "INSERT INTO users (email, password_hash, role, is_active, email_verified) VALUES ('admin@vuva.example', '${ARGON2_HASH}', 'admin', true, true) ON CONFLICT (email) DO NOTHING;"
else
	${PSQL} -d newspaper_db -c "INSERT INTO users (email, password_hash, role, is_active, email_verified) VALUES ('admin@vuva.example', '${ARGON2_HASH}', 'admin', true, true) ON CONFLICT (email) DO NOTHING;"
fi

echo "Done."
