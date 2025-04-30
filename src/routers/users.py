from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.database import get_async_session
from models.user_schemas import UserCreate, UserInfo
from oauth.schemas import Token
from src.oauth.jwt_utils import create_access_token_from_user
from src.cruds.users_crud import (
    get_user_by_login,
    create_user,
    authenticate_user,
    get_current_user,
)

router = APIRouter()


@router.post("/new", response_model=Token, summary="Register a new user")
async def post_new_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_async_session),
) -> Token:
    """
    Create a new user account and return an access token for that user.

    - **user**: User creation data (login, password, optional username)
    - **returns**: JWT access token and token type
    """
    existing_user = await get_user_by_login(db, user.login)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with such login already exists!",
        )

    created_user = await create_user(db, user)
    issued_token = create_access_token_from_user(created_user)

    return Token(access_token=issued_token, token_type="bearer")


@router.post("/token", response_model=Token, summary="Log in with credentials")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_async_session),
) -> Token:
    """
    Authenticate a user and return an access token.

    - **form_data**: OAuth2 form with username and password
    - **returns**: JWT access token and token type
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token_from_user(user)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserInfo, summary="Get current user profile")
async def get_self(
    current_user: Annotated[UserInfo, Depends(get_current_user)],
) -> UserInfo:
    """
    Get the currently authenticated user's information.

    - **returns**: User details (login, username, created_at, etc.)
    """
    return current_user
