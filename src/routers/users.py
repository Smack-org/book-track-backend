from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
import models.orm_models as models
from models.schemas import UserCreate, UserInfo
from oauth.schemas import Token
from oauth.utils import create_access_token
from oauth.auth_algorithm import oauth2_scheme, ALGORITHM
from typing import Annotated
from jose import jwt, JWTError
from sqlalchemy import select
from src.config import JWT_TOKEN_SECRET
from oauth.utils import verify_password, get_password_hash
import uuid
from datetime import datetime

router = APIRouter()


async def get_user_by_login(db: AsyncSession, login: str):
    stmt = select(models.User).where(models.User.login == login)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate) -> models.User:
    db_user = models.User(
        id=uuid.uuid4(),
        created_at=datetime.now(),
        **user.model_dump(exclude={"password"}),
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    await db.commit()
    db.refresh(db_user)
    return db_user


async def authenticate_user(db: AsyncSession, login: str, password: str) -> models.User:
    user = await get_user_by_login(db, login)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: AsyncSession = Depends(get_async_session)) -> UserInfo:
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

    user_info = UserInfo.model_validate(user)

    return user_info.to_dict()


@router.post("/new")
async def post_new_user(user: UserCreate,
                        db=Depends(get_async_session)) -> Token:
    if await get_user_by_login(db, user.login) is not None:
        raise HTTPException(400, "User with such login already exists!")

    created_user = await create_user(db, user)

    user_info = UserInfo.model_validate(created_user)
    issued_token = create_access_token(user_info.to_dict())

    return {"access_token": issued_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_async_session),
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_info = UserInfo.model_validate(user)

    access_token = create_access_token(
        data=user_info.to_dict()
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_self(current_user: Annotated[UserInfo, Depends(get_current_user)]) -> UserInfo:
    return current_user
