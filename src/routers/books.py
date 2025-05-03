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
    """
    Enrich a list of books with favourite metadata for a specific user.

    Adds 'is_favourite' and 'became_favourite_at' fields to each book in the results
    based on whether the book is marked as a favourite by the user.

    Args:
        books (dict): Dictionary containing book data with a 'results' list.
        user (UserInfo): The currently authenticated user.
        db (AsyncSession): Async SQLAlchemy database session.

    Returns:
        dict: The enriched books dictionary with updated 'results'.
    """
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
    """
    Retrieve a list of books with optional filtering and enrichment for favourites.

    Uses Gutendex API to fetch books and enriches them with favourite status for
    the authenticated user.

    Args:
        params (ListBooksParams): Query parameters for filtering/sorting books.
        client (GutendexClient): Client for interacting with Gutendex API.
        user (UserInfo): The currently authenticated user.
        db (AsyncSession): Async SQLAlchemy session.

    Returns:
        EnrichedBooksList: List of books with additional user-specific metadata.
    """
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
    """
    Retrieve a single book by its ID and enrich it with favourite metadata.

    Fetches book metadata from Gutendex API and annotates it with the
    user's favourite status.

    Args:
        id (int): The ID of the book to retrieve.
        client (GutendexClient): Gutendex API client.
        user (UserInfo): The currently authenticated user.
        db (AsyncSession): Async SQLAlchemy session.

    Returns:
        BookEnriched: Book data enriched with favourite status.

    Raises:
        HTTPException (404): If the book is not found in Gutendex.
    """
    try:
        data = await client.get_book(id)
        is_favourite, became_fav_at = await book_favourite_of_user(user, id, db)
        return BookEnriched(**data,
                            is_favourite=is_favourite,
                            became_favourite_at=became_fav_at)
    except httpx.HTTPStatusError as exc:
        httpx_error_to_fastapi_error(exc, "Book not found")
