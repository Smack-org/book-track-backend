from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from src.routers import books, favourites, reading_list, users
from config import APP_META

app = FastAPI(**APP_META)

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
app.include_router(users.router, prefix="/users", tags=["users"])

Instrumentator().instrument(app).expose(app)
