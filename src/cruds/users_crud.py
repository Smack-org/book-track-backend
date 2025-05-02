from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
from jose import jwt, JWTError
from datetime import datetime
import uuid

from src.database import get_async_session
import src.models.orm_models as models
from src.models.user_schemas import UserCreate, UserInfo
from src.oauth.password_utils import verify_password, get_password_hash
from src.config import JWT_TOKEN_SECRET
from src.oauth.auth_algorithm import ALGORITHM

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


async def get_user_by_login(db: AsyncSession, login: str) -> models.User | None:
    """
    Retrieve a user by login from the database.

    :param db: Async database session
    :param login: Login (username/email) to search
    :return: User instance or None if not found
    """
    stmt = select(models.User).where(models.User.login == login)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate) -> models.User:
    """
    Create and persist a new user in the database.

    :param db: Async database session
    :param user: User creation data
    :return: Created User instance
    """
    db_user = models.User(
        id=uuid.uuid4(),
        created_at=datetime.now(),
        **user.model_dump(exclude={"password"}),
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate_user(
    db: AsyncSession, login: str, password: str
) -> models.User | None:
    """
    Authenticate a user by login and password.

    :param db: Async database session
    :param login: Login of the user
    :param password: Plain password to verify
    :return: Authenticated User instance or None
    """
    user = await get_user_by_login(db, login)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_async_session),
) -> UserInfo:
    """
    Extract the currently authenticated user from the token.

    :param token: Bearer JWT access token
    :param db: Async database session
    :return: Pydantic UserInfo object representing the current user
    :raises HTTPException: If the token is invalid or user is not found
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_TOKEN_SECRET, algorithms=[ALGORITHM])
        login: str = payload.get("login")
        if login is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await get_user_by_login(db, login=login)
    if user is None:
        raise credentials_exception

    return user
