-- liquibase formatted sql

-- changeset catorleader:006-create-log-table
CREATE TABLE log
(
    action  action,
    user_id uuid,
    info varchar(1024)
);

ALTER TABLE log
    ADD CONSTRAINT fk_log_user FOREIGN KEY (user_id)
        REFERENCES "user" (id);

-- DROP TABLE IF EXISTS log CASCADE;
