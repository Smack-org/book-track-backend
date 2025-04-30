from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from src.config import JWT_TOKEN_SECRET
from .auth_algorithm import ALGORITHM
from src.models.user_schemas import UserBase

DEFAULT_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
    secret_key: str = JWT_TOKEN_SECRET,
    algorithm: str = ALGORITHM,
) -> str:
    """
    We need these comments so Radon does not spoil us CI.
    Create a JWT access token with optional expiration delta.

    Args:
        data (dict): The payload data to encode in the token.
        expires_delta (Optional[timedelta]): The duration until the token expires.
        secret_key (str): Secret key for signing the token.
        algorithm (str): JWT algorithm to use.

    Returns:
        str: Encoded JWT access token.
    """
    now = datetime.now()
    expire = now + (expires_delta or timedelta(minutes=DEFAULT_TOKEN_EXPIRE_MINUTES))
    payload = data.copy()
    payload.update({"exp": expire})

    return jwt.encode(payload, secret_key, algorithm=algorithm)


def create_access_token_from_user(user: UserBase) -> str:
    return create_access_token({
        "login": user.login
    })
