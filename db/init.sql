
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Create the role (user) 'tester' with a password 'postgres'
CREATE ROLE tester WITH LOGIN PASSWORD 'postgres';

-- Grant all privileges on all tables in the 'public' schema to the 'postgres' role
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tester;

-- Alter the ownership of the 'public' schema to 'postgres'
ALTER SCHEMA public OWNER TO tester;

-- Drop the existing database if it exists
DROP DATABASE IF EXISTS "users-db";

-- Create the database 'UserIdentity-db-test' owned by the 'postgres' role
CREATE DATABASE "users-db" OWNER tester;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
