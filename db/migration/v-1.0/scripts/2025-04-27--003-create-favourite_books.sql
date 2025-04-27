-- liquibase formatted sql

-- changeset catorleader:004-create-favourite_books-table
CREATE TABLE favourite_books
(
    book_id    integer,
    user_id    uuid,
    created_at timestamp,
    updated_at timestamp,
    PRIMARY KEY (book_id, user_id)
);

ALTER TABLE favourite_books
    ADD CONSTRAINT fk_favourite_books_user FOREIGN KEY (user_id)
        REFERENCES "user" (id);

-- DROP TABLE IF EXISTS favourite_books CASCADE;
