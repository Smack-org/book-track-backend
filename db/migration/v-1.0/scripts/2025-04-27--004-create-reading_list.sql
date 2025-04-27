-- liquibase formatted sql

-- changeset catorleader:005-create-reading_list-table
CREATE TABLE reading_list
(
    book_id    integer,
    user_id    uuid,
    status     reading_status,
    created_at timestamp,
    updated_at timestamp,
    PRIMARY KEY (book_id, user_id)
);

ALTER TABLE reading_list
    ADD CONSTRAINT fk_reading_list_user FOREIGN KEY (user_id)
        REFERENCES "user" (id);

-- DROP TABLE IF EXISTS reading_list CASCADE;
