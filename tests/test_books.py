from .conftest import API


def test_favourites_flow(api: API):
    # Step 1: Register & login
    response = api.register_user("books_tester", "StrongP@ss123", "Fav User")
    assert response.status_code == 200, f"Register failed: {response.text}"
    token = response.json().get("access_token")
    assert token, "No token received on registration"

    # Step 2: Add a favourite book
    response = api.add_favourite(token, book_id=84)  # Pride and Prejudice (PG)
    assert response.status_code == 201, f"Add fav failed: {response.text}"
    fav = response.json()
    assert fav["book"]["id"] == 84
    api.set_token(token)

    # Step 3: Get book
    response = api.get_book(84)
    assert response.status_code == 200, f"Get book failed: {response.text}"
    book = response.json()
    assert book['is_favourite'] is True

    # Step 4: Get Multiple books
    response = api.get_books()
    assert response.status_code == 200, f"Get book failed: {response.text}"
    books = response.json()['results']
    target = next((b for b in books if b['id'] == 84), None)

    assert target is not None, f"Book with ID {84} not found in book list"
    assert target['is_favourite'] is True, f"Book {84} is not marked as favourite"

    # Step 5: Remove from favourites
    response = api.remove_favourite(token, book_id=84)
    assert response.status_code == 204, f"Delete fav failed: {response.text}"

    # Step 6: Confirm deletion
    response = api.get_book(84)
    assert response.status_code == 200, f"Get book failed: {response.text}"
    book = response.json()
    assert book['is_favourite'] is False
