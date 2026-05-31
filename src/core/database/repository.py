from abc import ABC
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.base import CoreModel


class BaseRepo(ABC):
    """
    Abstract class for working with database models.
    It provides basic methods for CRUD operations on a specific database model.
    Attributes:
        _session_maker (async_sessionmaker): An instance of async_sessionmaker for creating database sessions.
        _model (CoreModel): The database model that this repository will manage.
    """

    def __init__(self, model: type[CoreModel], session: AsyncSession) -> None:
        self._session = session
        self._model = model

    async def get_all(self, limit: int = 100) -> list[CoreModel]:
        """
        Creates DB session and returns a list of all models.
        :param limit:
        :return:
        """
        query = select(self._model).limit(limit)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_by_pk(self, pk: int) -> Optional[CoreModel]:
        """
        Creates DB session and returns a single model by its primary key.
        :param pk:
        :return:
        """
        query = select(self._model).where(self._model.id == pk)
        result = await self._session.execute(query)
        return result.scalars().one_or_none()

    async def create(self, model: CoreModel) -> CoreModel:
        """
        Creates DB session and returns a single model by its primary key.
        :param model:
        :return:
        """
        self._session.add(model)
        await self._session.commit()
        await self._session.flush()
        return model

    async def update(self, model: CoreModel) -> CoreModel:
        """
        Updates DB session and returns a single model by its primary key.
        :param model:
        :return:
        """
        await self._session.commit()
        await self._session.refresh(model)
        return model