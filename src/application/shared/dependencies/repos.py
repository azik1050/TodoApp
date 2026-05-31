from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.shared.dependencies.session import get_session
from application.task.models import TaskModel
from application.task.repositories import (
    TaskRepo,
    TaskCommentRepo,
    TaskStatusHistoryRepo,
)


def get_task_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskRepo:
    return TaskRepo(TaskModel, session)


def get_task_comment_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskCommentRepo:
    return TaskCommentRepo(TaskModel, session)


def get_task_status_history_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TaskStatusHistoryRepo:
    return TaskStatusHistoryRepo(TaskModel, session)