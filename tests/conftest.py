import httpx
import pytest


class API:
    def __init__(self, base_url="http://api:8000"):
        """Initialize the API client with a base URL."""
        self.client = httpx.Client(base_url=base_url)
        self.token = None

    def register_user(self, login: str, password: str, username: str):
        """
        Register a new user.

        Args:
            login: User login identifier.
            password: User password.
            username: Display name for the user.

        Returns:
            HTTP response object.
        """
        return self.client.post("/users/new", json={
            "login": login,
            "password": password,
            "username": username,
        })

    def login(self, username: str, password: str):
        """
        Authenticate a user and store the access token.

        Args:
            username: Login identifier.
            password: Password.

        Returns:
            HTTP response object containing access token if successful.
        """
        response = self.client.post("/users/token", data={
            "username": username,
            "password": password,
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]
        return response

    def set_token(self, token):
        self.token = token

    def _auth_headers(self):
        """Generate authorization headers using the stored token."""
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def get_reading_list(self, offset: int = 0, limit: int = 20, status: str = "all"):
        """
        Retrieve the user's reading list.

        Args:
            offset: Pagination offset.
            limit: Number of items to return.
            status: Filter by reading status.

        Returns:
            HTTP response object with the reading list.
        """
        params = {"offset": offset, "limit": limit, "status": status}
        return self.client.get("/reading-list/", headers=self._auth_headers(), params=params)

    def add_book(self, book_id: int, status: str):
        """
        Add a book to the reading list.

        Args:
            book_id: ID of the book to add.
            status: Reading status to assign.

        Returns:
            HTTP response object.
        """
        return self.client.post("/reading-list/", headers=self._auth_headers(), json={
            "book_id": book_id,
            "status": status,
        })

    def update_book(self, book_id: int, status: str):
        """
        Update the reading status of a book.

        Args:
            book_id: ID of the book.
            status: New reading status.

        Returns:
            HTTP response object.
        """
        return self.client.patch(f"/reading-list/{book_id}", headers=self._auth_headers(), json={
            "status": status,
        })

    def delete_book(self, book_id: int):
        """
        Remove a book from the reading list.

        Args:
            book_id: ID of the book to remove.

        Returns:
            HTTP response object.
        """
        return self.client.delete(f"/reading-list/{book_id}", headers=self._auth_headers())

    def get_favourites(self, token: str, offset: int = 0, limit: int = 20):
        """
        Retrieve the user's favourite books.

        Args:
            token: Authorization token.
            offset: Pagination offset.
            limit: Number of items to return.

        Returns:
            HTTP response object with the list of favourite books.
        """
        headers = {"Authorization": f"Bearer {token}"}
        params = {"offset": offset, "limit": limit}
        return self.client.get("/favourites/", headers=headers, params=params)

    def add_favourite(self, token: str, book_id: int):
        """
        Add a book to the favourites list.

        Args:
            token: Authorization token.
            book_id: ID of the book to add.

        Returns:
            HTTP response object.
        """
        headers = {"Authorization": f"Bearer {token}"}
        json_body = {"book_id": book_id}
        return self.client.post("/favourites/", headers=headers, json=json_body)

    def remove_favourite(self, token: str, book_id: int):
        """
        Remove a book from the favourites list.

        Args:
            token: Authorization token.
            book_id: ID of the book to remove.

        Returns:
            HTTP response object.
        """
        headers = {"Authorization": f"Bearer {token}"}
        return self.client.delete(f"/favourites/{book_id}", headers=headers)

    def get_profile(self):
        """
        Retrieve the profile of the currently authenticated user.

        Returns:
            HTTP response object containing user profile data.
        """
        return self.client.get("/users/me", headers=self._auth_headers())

    def get_book(self, book_id: int):
        """
        Retrieve the book from gutindex, with field whether it is favourite or not.

        Returns:
            HTTP response object containing user profile data.
        """
        return self.client.get(f"/books/{book_id}", headers=self._auth_headers())

    def get_books(self, page=1):
        """
        Retrieve the book from gutindex, with field whether it is favourite or not.

        Returns:
            HTTP response object containing user profile data.
        """
        return self.client.get("/books/", headers=self._auth_headers(), params={"page": page})

    def stop(self):
        """
        Signal the test server to stop (used for E2E cleanup).

        Returns:
            HTTP response object.
        """
        return self.client.get("/e2e/die")

    def close(self):
        """Close the underlying HTTP client."""
        self.client.close()


@pytest.fixture
def api():
    client = API()
    yield client
    client.close()


def pytest_sessionfinish(session, exitstatus):
    """Called after the whole test run completes."""
    API().stop()
