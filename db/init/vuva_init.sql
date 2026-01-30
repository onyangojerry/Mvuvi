-- Initialization script executed by Postgres container on first start
-- Creates application role 'vuva_app' with a default password and grants basic privileges.

-- Change the password before using in production.
DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'vuva_app') THEN
    CREATE ROLE vuva_app LOGIN PASSWORD 'vuva_app_pwd';
  END IF;
END$$;

-- Ensure database exists (Postgres container may already create POSTGRES_DB)
-- The container will create 'newspaper_db' as POSTGRES_DB by env; grant privileges to role
GRANT CONNECT ON DATABASE newspaper_db TO vuva_app;

\c newspaper_db

GRANT USAGE ON SCHEMA public TO vuva_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO vuva_app;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO vuva_app;
