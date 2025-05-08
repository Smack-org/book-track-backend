import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.models.user_schemas import UserCreate
from src.cruds.users_crud import get_current_user, authenticate_user, create_user
from src.oauth.password_utils import verify_password


# Helper Fixtures

@pytest.fixture
def mock_db():
    """Fixture to mock database session"""
    return AsyncMock()


@pytest.fixture
def mock_user():
    """Fixture to create a mock user"""
    user = MagicMock()
    user.hashed_password = "hashed_pass"
    return user


# Test Functions

@pytest.mark.asyncio
async def test_create_user(mock_db):
    """Test user creation and verify correct interactions with the db"""
    user_in = UserCreate(login="testuser", email="test@example.com", password="testpass")

    with patch("src.oauth.password_utils.get_password_hash", return_value="hashed_pass"):
        user = await create_user(mock_db, user_in)

    # Assert that the user is created correctly
    assert user.login == user_in.login
    assert verify_password(user_in.password, user.hashed_password)

    # Verify DB methods were called correctly
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once_with(user)


@patch("src.cruds.users_crud.verify_password", return_value=True)
@patch("src.cruds.users_crud.get_user_by_login")
@pytest.mark.asyncio
async def test_authenticate_user_success(mock_get_user_by_login,
                                         mock_db, mock_user):
    """Test that the user can be successfully authenticated"""
    mock_get_user_by_login.return_value = mock_user

    result = await authenticate_user(mock_db, "testuser", "testpass")

    # Assert that the correct user is returned
    assert result == mock_user


@patch("src.cruds.users_crud.verify_password", return_value=False)
@patch("src.cruds.users_crud.get_user_by_login")
@pytest.mark.asyncio
async def test_authenticate_user_failure(mock_get_user_by_login,
                                         mock_db, mock_user):
    """Test that authentication fails when incorrect password is provided"""
    mock_get_user_by_login.return_value = mock_user

    result = await authenticate_user(mock_db, "testuser", "wrongpass")

    # Assert that None is returned for failed authentication
    assert result is None


@pytest.mark.asyncio
async def test_get_current_user_valid_token(mock_db, mock_user):
    """Test that current user is retrieved correctly when a valid token is provided"""
    mock_token = "mocktoken"

    with patch("src.oauth.jwt_utils.jwt.decode", return_value={"login": "testuser"}), \
         patch("src.cruds.users_crud.get_user_by_login", return_value=mock_user):
        user = await get_current_user(mock_token, db=mock_db)

    # Assert that the correct user is returned
    assert user == mock_user


@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    """Test that an exception is raised when an invalid token is provided"""
    with patch("src.oauth.jwt_utils.jwt.decode", side_effect=Exception):
        with pytest.raises(Exception):
            await get_current_user("invalidtoken", db=AsyncMock())
