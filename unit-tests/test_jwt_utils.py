from datetime import timedelta, datetime
from jose import jwt

from src.oauth.jwt_utils import create_access_token, create_access_token_from_user
from src.models.user_schemas import UserBase
from src.config import JWT_TOKEN_SECRET
from src.oauth.auth_algorithm import ALGORITHM


def test_create_access_token_generates_valid_token():
    now = datetime.now()
    data = {"sub": "user123"}
    token = create_access_token(data)

    # Decode the token to verify contents
    decoded = jwt.decode(token, JWT_TOKEN_SECRET, algorithms=[ALGORITHM])

    assert decoded["sub"] == "user123"
    assert "exp" in decoded

    # Convert the 'exp' from the token (Unix timestamp) to datetime
    exp = datetime.fromtimestamp(decoded["exp"])

    assert now < exp


def test_create_access_token_with_custom_expiry():
    data = {"role": "admin"}
    expires_delta = timedelta(minutes=60)
    token = create_access_token(data, expires_delta=expires_delta)
    decoded = jwt.decode(token, JWT_TOKEN_SECRET, algorithms=[ALGORITHM])

    assert decoded["role"] == "admin"

    exp = datetime.fromtimestamp(decoded["exp"])
    assert datetime.now() < exp


def test_create_access_token_from_user():
    user = UserBase(login="test_user")
    token = create_access_token_from_user(user)
    decoded = jwt.decode(token, JWT_TOKEN_SECRET, algorithms=[ALGORITHM])

    assert decoded["login"] == "test_user"
    assert "exp" in decoded
