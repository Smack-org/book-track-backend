from datetime import datetime
from fastapi import APIRouter
from src.models.schemas import (
    ReadingListEntry,
    ReadingListEntryCreate,
    ReadingListEntryUpdate,
)
from typing import List

from src.models.schemas import Book

router = APIRouter()

fake_reading_list_db = []


@router.get("/", response_model=List[ReadingListEntry])
async def get_reading_list(offset: int = 0, limit: int = 20,
                           status: str = "all"):
    filtered = [entry for entry in fake_reading_list_db
                if status == "all" or entry.status == status]
    return filtered[offset:offset + limit]


@router.post("/", response_model=ReadingListEntry, status_code=201)
async def add_to_reading_list(entry: ReadingListEntryCreate):
    new_entry = ReadingListEntry(
        book=Book(id=entry.book_id, title="Example Book", media_type="text",
                  download_count=0),
        status=entry.status,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    fake_reading_list_db.append(new_entry)
    return new_entry


@router.patch("/{book_id}", response_model=ReadingListEntry)
async def update_reading_status(book_id: int, update: ReadingListEntryUpdate):
    # Implement update logic
    return ReadingListEntry(
        book=Book(id=book_id, title="Example Book", media_type="text",
                  download_count=0),
        status=update.status,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@router.delete("/{book_id}", status_code=204)
async def remove_from_reading_list(book_id: int):
    # Implement deletion logic
    return
