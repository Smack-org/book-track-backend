-- liquibase formatted sql

-- changeset catorleader:001-create-reading_status-enum
CREATE TYPE reading_status AS ENUM ('want_to_read', 'reading', 'done');

-- DROP TYPE IF EXISTS reading_status;

-- changeset catorleader:002-create-action-enum
CREATE TYPE "action" AS ENUM ('create_account', 'add_favourite', 'remove_favourite', 'add_to_reading_list', 'change_reading_status', 'remove_from_reading_list');

-- DROP TYPE IF EXISTS actions;
