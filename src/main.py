from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager

from src.routers import books, favourites, reading_list, users
from config import APP_META, IS_E2E
from coverage_setup import start_cov, stop_cov


@asynccontextmanager
async def lifespan(app: FastAPI):
    if IS_E2E:
        start_cov()
        yield
        stop_cov()


app = FastAPI(
    **APP_META,
    lifespan=lifespan
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
app.include_router(users.router, prefix="/users", tags=["users"])

Instrumentator().instrument(app).expose(app)
