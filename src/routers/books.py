import httpx
from fastapi import APIRouter, Depends

from src.clients.gutendex_client import GutendexClient, get_gutendex_client
from src.models.schemas import Book, BooksList, Error, ListBooksParams
from .error_conversions import httpx_error_to_fastapi_error

router = APIRouter()


@router.get("/", response_model=BooksList)
async def list_books(
    params: ListBooksParams = Depends(),
    client: GutendexClient = Depends(get_gutendex_client),
):
    try:
        data = await client.list_books(**params.model_dump(exclude_none=True))
        return BooksList(**data)
    except httpx.HTTPStatusError as exc:
        httpx_error_to_fastapi_error(exc, "Books are not found")


@router.get("/{id}", response_model=Book, responses={404: {"model": Error}})
async def get_book(
    id: int,
    client: GutendexClient = Depends(get_gutendex_client),
):
    try:
        data = await client.get_book(id)
        return Book(**data)
    except httpx.HTTPStatusError as exc:
        httpx_error_to_fastapi_error(exc, "Book not found")
