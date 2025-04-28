from datetime import datetime

from fastapi import APIRouter
from src.models.schemas import Book, FavouriteBook, BookID
from typing import List


router = APIRouter()

# Temporary storage for example
fake_favourites_db = []


@router.get("/", response_model=List[FavouriteBook])
async def get_favourites(offset: int = 0, limit: int = 20):
    return fake_favourites_db[offset: offset + limit]


@router.post("/", response_model=FavouriteBook, status_code=201)
async def add_favourite(book: BookID):
    favourite = FavouriteBook(
        book=Book(id=book.book_id, title="Example Book", media_type="text",
                  download_count=0),
        added_at=datetime.now()
    )
    fake_favourites_db.append(favourite)
    return favourite


@router.delete("/{book_id}", status_code=204)
async def remove_favourite(book_id: int):
    # Implement deletion logic
    return
