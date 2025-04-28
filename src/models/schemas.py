from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict

from pydantic import BaseModel


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
