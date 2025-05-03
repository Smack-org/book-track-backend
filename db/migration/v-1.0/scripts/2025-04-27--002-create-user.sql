-- liquibase formatted sql

-- changeset catorleader:003-create-user-table
CREATE TABLE "user" (
    id uuid PRIMARY KEY,
    login varchar2(1024) UNIQUE,
    hashed_password varchar2(1024),
    username varchar2(1024),
    created_at timestamp
);

-- DROP TABLE IF EXISTS "user";
