from .conftest import API


def test_user_registration_flow():
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

    # Step 4: Try to login under non-existent user
    response = api.login("I_do_not_exist!", "My_password_is_nonsense!")
    assert response.status_code == 401, "Unregistered user managed to login, how come so bad?"

    # Step 5: try to register already existent user
    response = api.register_user("e2etestuser", "some_new_password", "Name again")
    assert response.status_code != 200, "User managed to register twice. How come so bad?"
    assert len(response.json()) != 0, "token received on registration of already existent user"

    # Step 6: try to register a user with small password
    response = api.register_user("e2etestuser", "123", "Some name, hz")
    assert response.status_code != 200, "User managed to register with bad pass. How come so bad?"

    api.stop()

    api.close()
