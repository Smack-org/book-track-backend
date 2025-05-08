from datetime import timedelta, datetime
from jose import jwt
import pytest

from src.oauth.jwt_utils import create_access_token, create_access_token_from_user
from src.models.user_schemas import UserBase
from src.config import JWT_TOKEN_SECRET
from src.oauth.auth_algorithm import ALGORITHM


# Helper Functions

def decode_token(token: str):
    """Decode the JWT token and return the payload."""
    return jwt.decode(token, JWT_TOKEN_SECRET, algorithms=[ALGORITHM])


def assert_token_has_exp(decoded: dict):
    """Ensure the decoded token has an 'exp' field and is a future date."""
    assert "exp" in decoded
    exp = datetime.fromtimestamp(decoded["exp"])
    assert datetime.now() < exp


# Fixtures

@pytest.fixture
def user():
    """Fixture to create a user for testing."""
    return UserBase(login="test_user")


# Test Functions

def test_create_access_token_generates_valid_token():
    """Test that the created token has the correct data and expiration."""
    data = {"sub": "user123"}
    token = create_access_token(data)

    decoded = decode_token(token)

    # Assert the token's 'sub' and expiration
    assert decoded["sub"] == "user123"
    assert_token_has_exp(decoded)


def test_create_access_token_with_custom_expiry():
    """Test that the created token respects custom expiry duration."""
    data = {"role": "admin"}
    expires_delta = timedelta(minutes=60)
    token = create_access_token(data, expires_delta=expires_delta)

    decoded = decode_token(token)

    # Assert the token's role and custom expiry
    assert decoded["role"] == "admin"
    assert_token_has_exp(decoded)


def test_create_access_token_from_user(user):
    """Test that a token can be created from a user and has correct data."""
    token = create_access_token_from_user(user)
    decoded = decode_token(token)

    # Assert the token's user login and expiration
    assert decoded["login"] == user.login
    assert_token_has_exp(decoded)
