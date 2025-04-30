from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict
from fastapi import Query
# from uuid import UUID

from pydantic import BaseModel, Field


class Person(BaseModel):
    name: str
    birth_year: Optional[int] = None
    death_year: Optional[int] = None


class BookBase(BaseModel):
    id: int
    title: str
    subjects: List[str] = []
    authors: List[Person] = []
    summaries: List[str] = []
    translators: List[Person] = []
    bookshelves: List[str] = []
    languages: List[str] = []
    copyright: Optional[bool] = None
    media_type: str
    formats: Dict[str, str] = {}
    download_count: int


class Book(BookBase):
    pass


class FavouriteBook(BaseModel):
    book: Book
    added_at: datetime


class ReadingStatus(str, Enum):
    WANT_TO_READ = "want_to_read"
    READING = "reading"
    DONE = "done"


class ReadingListEntryBase(BaseModel):
    status: ReadingStatus


class ReadingListEntryCreate(ReadingListEntryBase):
    book_id: int


class ReadingListEntryUpdate(ReadingListEntryBase):
    pass


class ReadingListEntry(ReadingListEntryBase):
    book: Book
    updated_at: datetime
    created_at: datetime


class BooksList(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[Book]


class BookID(BaseModel):
    book_id: int


class Error(BaseModel):
    code: int
    message: str


class ListBooksParams(BaseModel):
    page: int = Query(default=1)
    author_year_start: Optional[int] = Query(default=None)
    author_year_end: Optional[int] = Query(default=None)
    copyright: Optional[str] = Query(default=None)
    ids: Optional[str] = Query(default=None)
    languages: Optional[str] = Query(default=None)
    mime_type: Optional[str] = Query(default=None)
    search: Optional[str] = Query(default=None)
    topic: Optional[str] = Query(default=None)


class UserCreate(BaseModel):
    login: str
    password: str = Field(..., min_length=8)
    username: str | None = None


class UserInfo(BaseModel):
    login: str
    username: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

    def to_dict(self):
        return {
            "login": self.login,
            "username": self.username,
            "created_at": self.created_at.isoformat()
        }
