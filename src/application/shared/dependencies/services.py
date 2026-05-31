from fastapi import Depends
from typing import Annotated

from application.shared.dependencies.mappers import get_task_service_mapper
from application.shared.dependencies.repos import (
    get_task_repo,
    get_task_comment_repo,
    get_task_status_history_repo,
)
from application.task.mappers import TaskServiceMapper
from application.task.repositories import (
    TaskRepo,
    TaskStatusHistoryRepo,
    TaskCommentRepo,
)
from application.task.services import TaskService


def get_task_service(
    task_repo: Annotated[TaskRepo, Depends(get_task_repo)],
    task_comment_repo: Annotated[TaskCommentRepo, Depends(get_task_comment_repo)],
    task_status_history_repo: Annotated[
        TaskStatusHistoryRepo, Depends(get_task_status_history_repo)
    ],
    task_service_mapper: Annotated[TaskServiceMapper, Depends(get_task_service_mapper)],
) -> TaskService:
    return TaskService(
        task_repo=task_repo,
        task_comment_repo=task_comment_repo,
        task_status_history_repo=task_status_history_repo,
        task_service_mapper=task_service_mapper,
    )