-- liquibase formatted sql

-- changeset catorleader:003-create-user-table
CREATE TABLE "user" (
    id uuid PRIMARY KEY,
    name varchar UNIQUE,
    hashed_password varchar,
    username varchar,
    created_at timestamp
);

-- DROP TABLE IF EXISTS "user";
