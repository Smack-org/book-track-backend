-- liquibase formatted sql

-- changeset catorleader:002-create-trigger-log-user splitStatements:false endDelimiter:;
CREATE OR REPLACE FUNCTION trigger_log_user()
    RETURNS trigger AS
$$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO log(action, user_id, info)
        VALUES ('create_account',
                NEW.id,
                'Created account. Login: ' || NEW.login || ', Username: ' || NEW.username);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
-- DROP FUNCTION IF EXISTS trigger_log_user;

-- changeset catorleader:003-create-trigger-favourite-books-user splitStatements:false endDelimiter:;
CREATE OR REPLACE FUNCTION trigger_log_favourite_books()
    RETURNS trigger AS
$$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO log(action, user_id, info)
        VALUES ('add_favourite',
                NEW.user_id,
                'Added favourite book with book_id: ' || NEW.book_id);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO log(action, user_id, info)
        VALUES ('remove_favourite',
                OLD.user_id,
                'Removed favourite book with book_id: ' || OLD.book_id);
        RETURN OLD;
    ELSE
        RETURN NULL;
    END IF;
END;
$$ LANGUAGE plpgsql;
-- DROP FUNCTION IF EXISTS trigger_log_favourite_books;

-- changeset catorleader:004-create-trigger-reading-list-user splitStatements:false endDelimiter:;
CREATE OR REPLACE FUNCTION trigger_log_reading_list()
    RETURNS trigger AS
$$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO log(action, user_id, info)
        VALUES ('add_to_reading_list',
                NEW.user_id,
                'Added book (book_id: ' || NEW.book_id || ') to reading list with status: ' || NEW.status);
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO log(action, user_id, info)
        VALUES ('change_reading_status',
                NEW.user_id,
                'Changed book (book_id: ' || NEW.book_id || ') status from ' || OLD.status || ' to ' || NEW.status);
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO log(action, user_id, info)
        VALUES ('remove_from_reading_list',
                OLD.user_id,
                'Removed book (book_id: ' || OLD.book_id || ') from reading list');
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;
-- DROP FUNCTION IF EXISTS trigger_log_reading_list;
