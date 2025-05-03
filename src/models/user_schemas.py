"""
Module: user_models.py

This module defines Pydantic models for user-related operations,
including base properties, creation schema with validation,
and informational schema with timestamps and identifiers.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """
    Shared properties for user schemas.

    Attributes:
        login (str): Unique login identifier for the user.
        username (Optional[str]): Optional display username.
    """

    login: str = Field(
        ...,
        description="Unique login identifier for the user",
    )
    username: Optional[str] = Field(
        None,
        description="Optional display name for the user",
    )

    class Config:
        """
        Pydantic configuration for UserBase.
        """

        orm_mode = True  # Allow compatibility with ORMs
        anystr_strip_whitespace = True  # Strip whitespace on string fields


class UserCreate(UserBase):
    """
    Schema used when creating a new user.

    Inherits from UserBase and adds password validation.

    Attributes:
        password (str): Password string with minimum length enforcement.
    """

    password: str = Field(
        ...,
        min_length=8,
        description="Password with at least 8 characters",
    )


class UserInfo(UserBase):
    """
    Schema representing stored user information.

    Includes metadata about creation time and unique identifier.

    Attributes:
        created_at (datetime): Timestamp of user creation.
        id (str): Unique identifier (e.g., UUID) of the user.
    """

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp when the user was created",
    )
