from fastapi import FastAPI
from .routers import books, favourites, reading_list

app = FastAPI(
    title="Book Tracking API",
    description="Manage favourite books and reading lists",
    version="1.0.0"
)

app.include_router(favourites.router,
                   prefix="/favourites",
                   tags=["favourites"])
app.include_router(reading_list.router,
                   prefix="/reading-list",
                   tags=["reading-list"])
app.include_router(books.router,
                   prefix="/books",
                   tags=["books"])
