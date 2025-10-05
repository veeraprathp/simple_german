-- Initialize the simple_german database
-- This script is run when the PostgreSQL container starts

-- Create the database if it doesn't exist (this is handled by POSTGRES_DB env var)
-- But we can create additional schemas or extensions here if needed

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create any additional schemas if needed
-- CREATE SCHEMA IF NOT EXISTS cache;
-- CREATE SCHEMA IF NOT EXISTS analytics;

-- Set up any additional users or permissions
-- GRANT ALL PRIVILEGES ON DATABASE simple_german TO user;

-- The actual tables will be created by Alembic migrations
-- when the FastAPI application starts
