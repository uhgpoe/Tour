-- ==========================================================
-- Tourism Management System - PostgreSQL Database Setup
-- ==========================================================

-- 1. Create the Database (Run from PostgreSQL client / pgAdmin / psql)
CREATE DATABASE tourism_db WITH ENCODING 'UTF8';

-- 2. Connect to the database
\c tourism_db;

-- 3. Note: Django ORM generates and manages all tables automatically.
-- To initialize tables, run:
--   python manage.py migrate
--
-- To populate sample destinations, packages, reviews & demo accounts:
--   python manage.py seed_data
