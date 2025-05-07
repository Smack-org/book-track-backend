-- liquibase formatted sql

-- changeset catorleader:001-alter-log-table
ALTER TABLE log ADD COLUMN IF NOT EXISTS info varchar(1024);

-- ALTER TABLE log DROP COLUMN IF EXISTS info;
