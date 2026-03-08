from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from baseline.config import config

engine = create_async_engine(config.async_db_url)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession]:
    """Yield an async database session. Use with FastAPI Depends."""
    async with async_session_maker() as session:
        yield session
