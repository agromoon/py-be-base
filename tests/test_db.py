from sqlalchemy.ext.asyncio import AsyncSession

from baseline.db import async_session_maker


async def test_async_session_maker_creates_session() -> None:
    async with async_session_maker() as session:
        assert isinstance(session, AsyncSession)
