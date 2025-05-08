import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.models.user_schemas import UserCreate

from src.cruds.users_crud import get_current_user, authenticate_user, create_user
from src.oauth.password_utils import verify_password


@pytest.mark.asyncio
async def test_create_user():
    mock_db = AsyncMock()
    user_in = UserCreate(login="testuser", email="test@example.com", password="testpass")

    with patch("src.oauth.password_utils.get_password_hash", return_value="hashed_pass"):
        user = await create_user(mock_db, user_in)

    assert user.login == user_in.login
    assert verify_password(user_in.password, user.hashed_password)
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(user)


@patch("src.cruds.users_crud.verify_password", return_value=True)
@patch("src.cruds.users_crud.get_user_by_login")
@pytest.mark.asyncio
async def test_authenticate_user_success(mock_get_user_by_login, mock_verify_password):
    mock_db = AsyncMock()
    mock_user = MagicMock()
    mock_user.hashed_password = "hashed_pass"
    mock_get_user_by_login.return_value = mock_user

    result = await authenticate_user(mock_db, "testuser", "testpass")

    assert result == mock_user


@patch("src.cruds.users_crud.verify_password", return_value=False)
@patch("src.cruds.users_crud.get_user_by_login")
@pytest.mark.asyncio
async def test_authenticate_user_failure(mock_get_user_by_login, mock_verify_password):
    mock_db = AsyncMock()
    mock_user = MagicMock()
    mock_user.hashed_password = "hashed_pass"
    mock_get_user_by_login.return_value = mock_user

    result = await authenticate_user(mock_db, "testuser", "wrongpass")

    assert result is None


@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    mock_token = "mocktoken"
    mock_user = MagicMock()

    with patch("src.oauth.jwt_utils.jwt.decode", return_value={"login": "testuser"}), \
         patch("src.cruds.users_crud.get_user_by_login", return_value=mock_user):
        user = await get_current_user(mock_token, db=AsyncMock())

    assert user == mock_user


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    with patch("src.oauth.jwt_utils.jwt.decode", side_effect=Exception):
        with pytest.raises(Exception):
            await get_current_user("invalidtoken", db=AsyncMock())
