import httpx
import pytest


class API:
    def __init__(self, base_url="http://api:8000"):
        self.client = httpx.Client(base_url=base_url)
        self.token = None

    def register_user(self, login: str, password: str, username: str):
        return self.client.post("/users/new", json={
            "login": login,
            "password": password,
            "username": username,
        })

    def login(self, username: str, password: str):
        response = self.client.post("/users/token", data={
            "username": username,
            "password": password,
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]
        return response

    def _auth_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def get_reading_list(
        self,
        offset: int = 0,
        limit: int = 20,
        status: str = "all",  # matches ReadingStatus.ALL
    ):
        params = {"offset": offset, "limit": limit, "status": status}
        return self.client.get("/reading-list/", headers=self._auth_headers(), params=params)

    def add_book(self, book_id: int, status: str):
        return self.client.post("/reading-list/", headers=self._auth_headers(), json={
            "book_id": book_id,
            "status": status,
        })

    def update_book(self, book_id: int, status: str):
        return self.client.patch(f"/reading-list/{book_id}", headers=self._auth_headers(), json={
            "status": status,
        })

    def delete_book(self, book_id: int):
        return self.client.delete(f"/reading-list/{book_id}", headers=self._auth_headers())

    def get_favourites(
        self,
        token: str,
        offset: int = 0,
        limit: int = 20,
    ):
        headers = {"Authorization": f"Bearer {token}"}
        params = {"offset": offset, "limit": limit}
        return self.client.get("/favourites/", headers=headers, params=params)

    def add_favourite(
        self,
        token: str,
        book_id: int,
    ):
        headers = {"Authorization": f"Bearer {token}"}
        json_body = {"book_id": book_id}
        return self.client.post("/favourites/", headers=headers, json=json_body)

    def remove_favourite(
        self,
        token: str,
        book_id: int,
    ):
        headers = {"Authorization": f"Bearer {token}"}
        return self.client.delete(f"/favourites/{book_id}", headers=headers)

    def get_profile(self):
        return self.client.get("/users/me", headers=self._auth_headers())

    def stop(self):
        return self.client.get("/e2e/die")

    def close(self):
        self.client.close()


@pytest.fixture
def api():
    client = API()
    yield client
    client.close()


def pytest_sessionfinish(session, exitstatus):
    """Called after the whole test run completes."""
    API().stop()
