from abc import ABC

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.core.database.base import CoreModel


class BaseRepo(ABC):
    """
    Abstract class for working with database models.
    It provides basic methods for CRUD operations on a specific database model.
    Attributes:
        _session_maker (async_sessionmaker): An instance of async_sessionmaker for creating database sessions.
        _model (CoreModel): The database model that this repository will manage.
    """

    def __init__(self, model: CoreModel, session_maker: async_sessionmaker):
        self._session_maker = session_maker
        self._model = model

    async def get_all(self, limit: int = 100) -> list[CoreModel]:
        async with self._session_maker() as session:
            query = select(self._model).limit(limit)
            result = await session.execute(query)
        return list(result.scalars().all())

    async def get_by_pk(self, pk: int) -> None:
        async with self._session_maker() as session:
            query = delete(self._model).where(self._model.id == pk)
            await session.execute(query)
            