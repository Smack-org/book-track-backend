from .conftest import API


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
