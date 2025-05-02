import httpx


class API:
    def __init__(self, base_url="http://api:8000"):
        self.client = httpx.Client(base_url=base_url)

    def register_user(self, login: str, password: str, username: str):
        return self.client.post("/users/new", json={
            "login": login,
            "password": password,
            "username": username,
        })

    def login(self, username: str, password: str):
        return self.client.post("/users/token", data={
            "username": username,
            "password": password,
        })

    def get_profile(self, token: str):
        headers = {"Authorization": f"Bearer {token}"}
        return self.client.get("/users/me", headers=headers)

    def stop(self):
        return self.client.get("/e2e/die")

    def close(self):
        self.client.close()
