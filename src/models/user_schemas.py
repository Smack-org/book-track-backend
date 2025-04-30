from pydantic import BaseModel, Field
from datetime import datetime


class UserBase(BaseModel):
    login: str
    username: str | None = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserInfo(UserBase):
    created_at: datetime
