from .conftest import API


def test_favourites_flow(api: API):
    # Step 1: Register & login
    response = api.register_user("favourite_tester", "StrongP@ss123", "Fav User")
    assert response.status_code == 200, f"Register failed: {response.text}"
    token = response.json().get("access_token")
    assert token, "No token received on registration"

    # Step 2: Add a favourite book
    response = api.add_favourite(token, book_id=1342)  # Pride and Prejudice (PG)
    assert response.status_code == 201, f"Add fav failed: {response.text}"
    fav = response.json()
    assert fav["book"]["id"] == 1342

    # Step 3: Get favourites
    response = api.get_favourites(token)
    assert response.status_code == 200, f"Get favs failed: {response.text}"
    favs = response.json()
    assert any(f["book"]["id"] == 1342 for f in favs), "Expected book not in favourites"

    # Step 4: Remove from favourites
    response = api.remove_favourite(token, book_id=1342)
    assert response.status_code == 204, f"Delete fav failed: {response.text}"

    # Step 5: Confirm deletion
    response = api.get_favourites(token)
    assert response.status_code == 200
    favs = response.json()
    assert all(f["book"]["id"] != 1342 for f in favs), "Book still in favourites after delete"
