-- Create additional test schemas if needed
CREATE SCHEMA IF NOT EXISTS testschema;

-- Set up test-specific extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create test tables (optional)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);