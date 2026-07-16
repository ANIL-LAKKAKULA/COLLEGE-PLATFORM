"""
Async SQLAlchemy engine + session factory. Exposes `get_db()`, an async
generator dependency that yields a session per-request and closes it
afterward. Also the declarative Base that all models inherit from.
"""

from collections.abc import AsyncGenerator

from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

""" Connection manager to Database"""
engine = create_async_engine(
    settings.database_url,
    echo=(settings.app_env == "local"),  # log SQL in dev only
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: one session per request, always closed after."""
    async with AsyncSessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    """Every model in app/models/ inherits from this."""
