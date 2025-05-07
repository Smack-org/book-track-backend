-- liquibase formatted sql

-- changeset catorleader:001-alter-log-table
ALTER TABLE log ADD COLUMN created_at TIMESTAMP DEFAULT now();

-- ALTER TABLE log DROP COLUMN IF EXISTS created_at;
