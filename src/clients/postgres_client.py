import os
from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/bookdb")
database = Database(DATABASE_URL)

async def connect_db() -> None:
    if not database.is_connected:
        await database.connect()

async def disconnect_db() -> None:
    if database.is_connected:
        await database.disconnect()

async def get_db():
    if not database.is_connected:
        await database.connect()
    try:
        yield database
    finally:
        # не отключаем — пул живёт до shutdown
        pass

