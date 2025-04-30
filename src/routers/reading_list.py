from datetime import datetime
from typing import List
from .users import get_current_user, UserInfo

from fastapi import APIRouter, Depends

from src.models.schemas import Book
from src.models.schemas import (
    ReadingListEntry,
    ReadingListEntryCreate,
    ReadingListEntryUpdate,
)

router = APIRouter()

fake_reading_list_db = []


@router.get("/", response_model=List[ReadingListEntry])
async def get_reading_list(
          user: UserInfo = Depends(get_current_user),
          offset: int = 0, limit: int = 20, status: str = "all"):
    """
    Get the reading list of currently authorized user.

    - **returns**: User reading list
    """
    filtered = [
        entry
        for entry in fake_reading_list_db
        if status == "all" or entry.status == status
    ]
    return filtered[offset: offset + limit]


@router.post("/", response_model=ReadingListEntry, status_code=201)
async def add_to_reading_list(
          entry: ReadingListEntryCreate,
          user: UserInfo = Depends(get_current_user)):
    new_entry = ReadingListEntry(
        book=Book(
            id=entry.book_id, title="Example Book", media_type="text", download_count=0
        ),
        status=entry.status,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    fake_reading_list_db.append(new_entry)
    return new_entry


@router.patch("/{book_id}", response_model=ReadingListEntry)
async def update_reading_status(
          book_id: int, update: ReadingListEntryUpdate,
          user: UserInfo = Depends(get_current_user)):
    # Implement update logic
    return ReadingListEntry(
        book=Book(
            id=book_id, title="Example Book", media_type="text", download_count=0
        ),
        status=update.status,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@router.delete("/{book_id}", status_code=204)
async def remove_from_reading_list(book_id: int,
                                   user: UserInfo = Depends(get_current_user)):
    # Implement deletion logic
    return
