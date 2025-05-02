import uuid

from sqlalchemy import String, UUID, TIMESTAMP
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.functions import now

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    login = mapped_column(String(1024), unique=True, nullable=False)  # like login
    hashed_password = mapped_column(String(1024))
    username = mapped_column(String(1024))
    created_at = mapped_column(
        TIMESTAMP, index=True, nullable=False, server_default=now()
    )
