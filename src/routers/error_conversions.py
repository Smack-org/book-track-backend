import httpx
from fastapi import HTTPException


def httpx_error_to_fastapi_error(exc: httpx.HTTPStatusError, not_found_message: str):
    if exc.response.status_code == 404:
        raise HTTPException(status_code=404, detail=not_found_message)
    raise exc
