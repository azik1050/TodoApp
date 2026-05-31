from sqlalchemy.ext.asyncio import AsyncSession

from core.database.session import session_maker


async def get_session() -> AsyncSession:
    async with session_maker() as session:
        yield session