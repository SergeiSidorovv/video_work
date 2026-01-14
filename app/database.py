from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
import os

from .config import settings

use_null_pool = os.getenv("USE_NULL_POOL", "false").lower() == "true"

engine_kwargs = {
    "url": settings.database_url_asyncpg,
    "pool_pre_ping": True,
    "echo": False,
}

if use_null_pool:
    from sqlalchemy.pool import NullPool

    engine_kwargs["poolclass"] = NullPool

engine = create_async_engine(**engine_kwargs)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
