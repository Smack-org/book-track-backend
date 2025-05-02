from datetime import datetime
from typing import List
from .users import get_current_user, UserInfo

from src.database import get_async_session

from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncSession
from src.clients.gutendex_client import GutendexClient, get_gutendex_client

from fastapi import APIRouter, Depends, HTTPException, status

from src.models.schemas import Book, ReadingStatus
from src.models.schemas import (
    ReadingListEntry,
    ReadingListEntryCreate,
    ReadingListEntryUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[ReadingListEntry])
async def get_reading_list(
    offset: int = 0,
    limit: int = 20,
    status: ReadingStatus = ReadingStatus.ALL,
    user: UserInfo = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
    gut_client: GutendexClient = Depends(get_gutendex_client),
):
    """
    Get the reading list of currently authorized user.

    - **returns**: User reading list
    """
    if status == ReadingStatus.ALL:
        result = await session.execute(
            text("""SELECT book_id, status, created_at, updated_at FROM reading_list WHERE
                    user_id = :user_id ORDER BY updated_at DESC LIMIT :limit OFFSET :offset"""),
            {"user_id": str(user.id), "limit": limit, "offset": offset}
        )
    else:
        result = await session.execute(
            text("""SELECT book_id, status, created_at, updated_at FROM reading_list
                    WHERE user_id = :user_id AND status = :status
                    ORDER BY updated_at DESC LIMIT :limit OFFSET :offset"""),
            {"user_id": str(user.id), "status": status, "limit": limit, "offset": offset}
        )
    rows = result.all()
    reading_list: List[ReadingListEntry] = []
    for book_id, status, created_at, updated_at in rows:
        try:
            metadata = await gut_client.get_book(book_id)
        except Exception:
            raise HTTPException(status_code=404, detail=f"Book {book_id} not found in Gutendex")
        book = Book(**metadata)
        reading_list.append(ReadingListEntry(
            status=ReadingStatus(status),
            book=book,
            created_at=created_at,
            updated_at=updated_at,
        ))
    return reading_list

@router.post("/", response_model=ReadingListEntry, status_code=201)
async def add_to_reading_list(
          entry: ReadingListEntryCreate,
          user: UserInfo = Depends(get_current_user),
          session: AsyncSession = Depends(get_async_session),
          gut_client: GutendexClient = Depends(get_gutendex_client)):

    try:
        data = await gut_client.get_book(entry.book_id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Book {entry.book_id} not found in Gutendex")
    created_at = datetime.now()
    await session.execute(text(
        """INSERT INTO reading_list (book_id, user_id, status, created_at, updated_at)
        VALUES (:book_id, :user_id, :status, :created_at, :created_at)
        ON CONFLICT DO NOTHING"""),
        {"user_id": str(user.id), "book_id": entry.book_id, "status": entry.status.value, 
         "created_at": created_at})
    await session.commit()
    return ReadingListEntry(status=ReadingStatus(entry.status.value), book=Book(**data), updated_at=created_at, created_at=created_at)


@router.patch("/{book_id}", response_model=ReadingListEntry)
async def update_reading_status(
          book_id: int, update: ReadingListEntryUpdate,
          user: UserInfo = Depends(get_current_user),
          session: AsyncSession = Depends(get_async_session),
          gut_client: GutendexClient = Depends(get_gutendex_client)):
    
    try:
        data = await gut_client.get_book(book_id)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Book {book_id} not found in Gutendex")
        
    updated_at = datetime.now()
    created_at = await session.execute(text(
        """UPDATE reading_list SET status = :status, updated_at = :updated_at
        WHERE book_id = :book_id AND user_id = :user_id RETURNING created_at"""),
        {"book_id": book_id, "user_id": str(user.id), "status": update.status.value,
         "updated_at": updated_at}
    )
    await session.commit()

    return ReadingListEntry(status=update.status, book=Book(**data), updated_at=updated_at, created_at=created_at)

@router.delete("/{book_id}", status_code=204)
async def remove_from_reading_list(book_id: int,
                                   user: UserInfo = Depends(get_current_user),
                                   session: AsyncSession = Depends(get_async_session)):
    await session.execute(
        text("DELETE FROM reading_list WHERE user_id = :user_id AND book_id = :book_id"),
        {"user_id": str(user.id), "book_id": book_id}
    )
    await session.commit()
    return
