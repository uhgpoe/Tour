-- ==========================================================
-- Tourism Management System - MySQL Database Initialization
-- ==========================================================

-- 1. Create Database with full UTF-8 Unicode support
CREATE DATABASE IF NOT EXISTS `tourism_db` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 2. Select Database
USE `tourism_db`;

-- Note: Django's ORM automatically generates and manages all tables
-- through migrations. To initialize tables, run:
--   python manage.py migrate
--
-- To populate sample destinations, packages, reviews & admin:
--   python manage.py seed_data
