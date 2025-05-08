from src.oauth.password_utils import get_password_hash, verify_password


def test_password_hashing_sanity():
    password = "Smack-test-1234"

    hashed_pass = get_password_hash(password)
    assert hashed_pass != password

    assert verify_password(password, hashed_pass)
