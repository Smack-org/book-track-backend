from typing import Optional, Dict, Any, AsyncGenerator
import httpx
from async_lru import alru_cache


class GutendexClient:
    """
    A reusable async client for interacting with the
    Gutendex API (https://gutendex.com), using an async LRU cache
    for `get_book` and `list_books` calls.
    """

    BASE_URL = "https://gutendex.com"

    def __init__(self, client: httpx.AsyncClient | None = None):
        # Ensure the HTTP client follows redirects from Gutendex endpoints
        self._client = client or httpx.AsyncClient(
            base_url=self.BASE_URL,
            follow_redirects=True,
        )

    @alru_cache(maxsize=128)
    async def get_book(self, book_id: int) -> Dict[str, Any]:
        """
        Fetches a single book by ID from Gutendex.
        Uses an async LRU cache to avoid repeated requests for the same book.
        Raises HTTPStatusError on non-200 (including 404).
        """
        # Include trailing slash to avoid redirect
        response = await self._client.get(f"/books/{book_id}/")
        if response.status_code == 404:
            raise httpx.HTTPStatusError(
                message="Book not found",
                request=response.request,
                response=response,
            )
        response.raise_for_status()
        return response.json()

    @alru_cache(maxsize=64)
    async def list_books(
        self,
        page: int = 1,
        author_year_start: Optional[int] = None,
        author_year_end: Optional[int] = None,
        copyright: Optional[str] = None,
        ids: Optional[str] = None,
        languages: Optional[str] = None,
        mime_type: Optional[str] = None,
        search: Optional[str] = None,
        topic: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fetches a paginated list of books from Gutendex with optional filters.
        Uses an async LRU cache keyed on all method arguments.
        Returns the parsed JSON payload as a dict.
        """
        params: Dict[str, Any] = {"page": page}
        if author_year_start is not None:
            params["author_year_start"] = author_year_start
        if author_year_end is not None:
            params["author_year_end"] = author_year_end
        if copyright is not None:
            params["copyright"] = copyright
        if ids is not None:
            params["ids"] = ids
        if languages is not None:
            params["languages"] = languages
        if mime_type is not None:
            params["mime_type"] = mime_type
        if search is not None:
            params["search"] = search
        if topic is not None:
            params["topic"] = topic

        # Use trailing slash to avoid redirect
        response = await self._client.get("/books/", params=params)
        response.raise_for_status()
        return response.json()


async def get_gutendex_client() -> AsyncGenerator[GutendexClient, None]:
    """
    FastAPI dependency provider that yields a GutendexClient with
    a managed HTTPX AsyncClient.
    """
    async with httpx.AsyncClient(
        base_url=GutendexClient.BASE_URL,
        follow_redirects=True,
    ) as async_client:
        yield GutendexClient(async_client)

