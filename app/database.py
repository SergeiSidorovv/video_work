from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
import os

from .config import settings


engine_kwargs = {
    "url": settings.database_url_asyncpg,
    "pool_pre_ping": True,
    "echo": False,
}

engine = create_async_engine(**engine_kwargs)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
