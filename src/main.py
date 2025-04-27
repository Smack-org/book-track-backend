from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers import books, favourites, reading_list

app = FastAPI(
    title="Book Tracking API",
    description="Manage favourite books and reading lists",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(favourites.router, prefix="/favourites", tags=["favourites"])
app.include_router(reading_list.router, prefix="/reading-list", tags=["reading-list"])
app.include_router(books.router, prefix="/books", tags=["books"])
