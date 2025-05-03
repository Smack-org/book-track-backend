from datetime import datetime
from src.models.user_schemas import UserFromDB
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import text


async def get_all_favourites_of_user(user: UserFromDB, db: AsyncSession) \
                -> dict[int, datetime]:
    result = await db.execute(text(
        """SELECT book_id, created_at FROM favourite_books WHERE
        user_id = :user_id ORDER BY created_at DESC"""
        ), {"user_id": user.id},
    )
    rows = result.all()
    return {id: added_at for id, added_at in rows}


async def book_favourite_of_user(
    user: UserFromDB,
    book_id: int,
    db: AsyncSession
) -> tuple[bool, Optional[datetime]]:
    """
    Check if a book is in the user's favourites.

    Args:
        user: The user to check for.
        book_id: The ID of the book.
        db: Async database session.

    Returns:
        A tuple (exists, created_at) where:
            - exists: True if the favourite exists, else False.
            - created_at: Timestamp when it was added, or None if not found.
    """
    result = await db.execute(
        text("""
            SELECT created_at FROM favourite_books
            WHERE user_id = :user_id AND book_id = :book_id
        """),
        {"user_id": str(user.id), "book_id": book_id},
    )

    row = result.first()
    if row:
        return True, row[0]
    return False, None
