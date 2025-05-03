from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from sqlalchemy import text

from fastapi import APIRouter, Depends, HTTPException
from src.models.schemas import Book, FavouriteBook, BookID
from src.models.user_schemas import UserFromDB
from .users import get_current_user, UserInfo

from typing import List

from src.clients.gutendex_client import GutendexClient, get_gutendex_client

router = APIRouter()


@router.get("/", response_model=List[FavouriteBook])
async def get_favourites(
    offset: int = 0,
    limit: int = 20,
    user: UserFromDB = Depends(get_current_user),
    gut_client: GutendexClient = Depends(get_gutendex_client),
    db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(
        text(
            """SELECT book_id, created_at FROM favourite_books WHERE
             user_id = :user_id ORDER BY created_at DESC OFFSET :offset LIMIT :limit"""
        ),
        {"user_id": user.id, "offset": offset, "limit": limit},
    )
    rows = result.all()
    favourites: List[FavouriteBook] = []
    for book_id, added_at in rows:
        try:
            metadata = await gut_client.get_book(book_id)
        except Exception:
            raise HTTPException(
                status_code=404, detail=f"Book {book_id} not found in Gutendex"
            )
        book = Book(**metadata)
        favourites.append(FavouriteBook(book=book, added_at=added_at))
    return favourites


@router.post("/", response_model=FavouriteBook, status_code=201)
async def add_favourite(
    book: BookID,
    user: UserInfo = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
    gut_client: GutendexClient = Depends(get_gutendex_client),
):
    try:
        data = await gut_client.get_book(book.book_id)
    except Exception:
        raise HTTPException(
            status_code=404, detail=f"Book {book.book_id} not found in Gutendex"
        )

    added_at = datetime.now()
    await session.execute(
        text(
            "INSERT INTO favourite_books (user_id, book_id, created_at, updated_at)"
            " VALUES (:user_id, :book_id, :added_at, :added_at)"
            " ON CONFLICT DO NOTHING"
        ),
        {"user_id": str(user.id), "book_id": book.book_id, "added_at": added_at},
    )
    await session.commit()
    inserted_book = Book(**data)
    return FavouriteBook(book=inserted_book, added_at=added_at)


@router.delete("/{book_id}", status_code=204)
async def remove_favourite(
    book_id: int,
    user: UserInfo = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    await session.execute(
        text(
            "DELETE FROM favourite_books WHERE user_id = :user_id AND book_id = :book_id"
        ),
        {"user_id": str(user.id), "book_id": book_id},
    )
    await session.commit()
    return
