from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, Depends

from src.clients.gutendex_client import GutendexClient, get_gutendex_client
from src.models.schemas import Book, BooksList, Error

router = APIRouter()


@router.get("/", response_model=BooksList)
async def list_books(
    page: int = 1,
    author_year_start: Optional[int] = None,
    author_year_end: Optional[int] = None,
    copyright: Optional[str] = None,
    ids: Optional[str] = None,
    languages: Optional[str] = None,
    mime_type: Optional[str] = None,
    search: Optional[str] = None,
    topic: Optional[str] = None,
    client: GutendexClient = Depends(get_gutendex_client),
):
    data = await client.list_books(
        page=page,
        author_year_start=author_year_start,
        author_year_end=author_year_end,
        copyright=copyright,
        ids=ids,
        languages=languages,
        mime_type=mime_type,
        search=search,
        topic=topic,
    )
    return BooksList(**data)


@router.get("/{id}", response_model=Book, responses={404: {"model": Error}})
async def get_book(
    id: int,
    client: GutendexClient = Depends(get_gutendex_client),
):
    try:
        data = await client.get_book(id)
        return Book(**data)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise HTTPException(status_code=404, detail="Book not found")
        raise
