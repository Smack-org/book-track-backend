-- liquibase formatted sql

-- changeset catorleader:005-create-user-trigger
CREATE TRIGGER user_changes
    AFTER INSERT OR UPDATE OR DELETE
    ON "user"
    FOR EACH ROW
EXECUTE FUNCTION trigger_log_user();
-- DROP TRIGGER IF EXISTS user_changes;

-- changeset catorleader:006-create-favourite-books-trigger
CREATE TRIGGER favourite_books_changes
    AFTER INSERT OR DELETE
    ON favourite_books
    FOR EACH ROW
EXECUTE FUNCTION trigger_log_favourite_books();
-- DROP TRIGGER IF EXISTS user_changes;

-- changeset catorleader:007-create-reading-list-trigger
CREATE TRIGGER reading_list_changes
    AFTER INSERT OR UPDATE OR DELETE
    ON reading_list
    FOR EACH ROW
EXECUTE FUNCTION trigger_log_reading_list();
-- DROP TRIGGER IF EXISTS user_changes;
