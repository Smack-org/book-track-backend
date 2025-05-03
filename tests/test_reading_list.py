from .conftest import API


def test_reading_list_flow(api: API):
    # Step 1: Register and Login
    assert api.register_user("testuser", "testpass123", "Test User").status_code == 200
    login_res = api.login("testuser", "testpass123")
    assert login_res.status_code == 200
    assert api.token is not None

    # Step 2: Get empty reading list
    res = api.get_reading_list()
    assert res.status_code == 200
    assert res.json() == []

    # Step 3: Add a book (assume ID 84 exists in Gutendex)
    res = api.add_book(book_id=84, status="want_to_read")
    assert res.status_code == 201
    book_entry = res.json()
    assert book_entry["book"]["id"] == 84
    assert book_entry["status"] == "want_to_read"

    # Step 4: Get reading list with one entry
    res = api.get_reading_list()
    assert res.status_code == 200
    assert len(res.json()) == 1

    # Step 5: Update reading status
    res = api.update_book(book_id=84, status="reading")
    assert res.status_code == 200
    assert res.json()["status"] == "reading"

    # Check it can find it by status filter
    res = api.get_reading_list(status="want_to_read")
    assert res.status_code == 200
    assert len(res.json()) == 0

    res = api.get_reading_list(status="reading")
    assert res.status_code == 200
    assert len(res.json()) == 1

    # Step 6: Delete book
    res = api.delete_book(book_id=84)
    assert res.status_code == 204

    # Step 7: Confirm empty reading list again
    res = api.get_reading_list()
    assert res.status_code == 200
    assert res.json() == []
