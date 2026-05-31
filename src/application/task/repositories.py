from sqlalchemy import select

from application.task.models import TaskStatusHistoryModel, TaskCommentModel
from core.database.repository import BaseRepo
from typing import Optional


class TaskRepo(BaseRepo):
    """
    Repository for managing Task database model.
    Inherits from BaseRepo and provides methods for CRUD operations on Task model.
    """

    pass


class TaskCommentRepo(BaseRepo):
    """
    Repository for managing Task Comment database model.
    Inherits from BaseRepo and provides methods for CRUD operations on Task Comment model.
    """

    async def get_by_task_id(
        self,
        task_id: int,
    ) -> list[TaskStatusHistoryModel]:
        query = (
            select(TaskCommentModel)
            .where(TaskCommentModel.task_id == task_id)
            .order_by(TaskCommentModel.created_at.desc())
        )
        result = await self._session.execute(query)
        return result.scalars().all()


class TaskStatusHistoryRepo(BaseRepo):
    """
    Repository for managing TaskStatusHistory database model.
    Inherits from BaseRepo and provides methods for CRUD operations on TaskStatusHistory model.
    """

    async def get_by_task_id(
        self,
        task_id: int,
    ) -> list[TaskStatusHistoryModel]:
        query = (
            select(TaskStatusHistoryModel)
            .where(TaskStatusHistoryModel.task_id == task_id)
            .order_by(TaskStatusHistoryModel.created_at.desc())
        )
        result = await self._session.execute(query)
        return result.scalars().all()

    async def get_previous_task_status_by_task_id(
        self,
        task_id: int,
    ) -> Optional[TaskStatusHistoryModel]:
        query = (
            select(TaskStatusHistoryModel)
            .where(TaskStatusHistoryModel.task_id == task_id)
            .order_by(TaskStatusHistoryModel.created_at.desc())
            .limit(1)
        )
        result = await self._session.execute(query)
        return result.scalars().one_or_none()