import httpx
from fastapi import APIRouter, Depends

from src.clients.gutendex_client import GutendexClient, get_gutendex_client
from src.models.schemas import EnrichedBooksList, Error, ListBooksParams, BookEnriched
from .error_conversions import httpx_error_to_fastapi_error
from .users import get_current_user, UserInfo
from src.cruds.favourites_crud import get_all_favourites_of_user, book_favourite_of_user
from src.database import get_async_session, AsyncSession

router = APIRouter()


async def enrich_books(books, user, db):
    user_current_favs = await get_all_favourites_of_user(user, db)
    for book in books['results']:
        if book['id'] in user_current_favs:
            book['is_favourite'] = True
            book['became_favourite_at'] = user_current_favs[book['id']]
        else:
            book['is_favourite'] = False
            book['became_favourite_at'] = None
    return books


@router.get("/", response_model=EnrichedBooksList)
async def list_books(
    params: ListBooksParams = Depends(),
    client: GutendexClient = Depends(get_gutendex_client),
    user: UserInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    try:
        books = await client.list_books(**params.model_dump(exclude_none=True))
        enriched = await enrich_books(books, user, db)
        return EnrichedBooksList(**enriched)
    except httpx.HTTPStatusError as exc:
        httpx_error_to_fastapi_error(exc, "Books are not found")


@router.get("/{id}", response_model=BookEnriched, responses={404: {"model": Error}})
async def get_book(
    id: int,
    client: GutendexClient = Depends(get_gutendex_client),
    user: UserInfo = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    try:
        data = await client.get_book(id)
        is_favourite, became_fav_at = await book_favourite_of_user(user, id, db)
        return BookEnriched(**data,
                            is_favourite=is_favourite,
                            became_favourite_at=became_fav_at)
    except httpx.HTTPStatusError as exc:
        httpx_error_to_fastapi_error(exc, "Book not found")
