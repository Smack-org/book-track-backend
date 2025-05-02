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

    def close(self):
        self.client.close()


def test_user_flow_against_running_api():
    api = API()

    # Step 1: Register
    response = api.register_user("e2etestuser", "strongpassword123", "E2E Tester")
    assert response.status_code == 200, f"Register failed: {response.text}"
    token = response.json().get("access_token")
    assert token, "No token received on registration"

    # Step 2: Login
    response = api.login("e2etestuser", "strongpassword123")
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json().get("access_token")
    assert token, "No token received on login"

    # Step 3: Get profile
    response = api.get_profile(token)
    assert response.status_code == 200, f"/me failed: {response.text}"
    profile = response.json()
    assert profile["login"] == "e2etestuser"
    assert profile["username"] == "E2E Tester"

    api.close()
