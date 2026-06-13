from fastapi import APIRouter
from fastapi.params import Depends
from typing import Annotated

from application.shared.dependencies.services import get_task_service
from application.task.schemas import (
    TaskWrite,
    TaskRead,
    TaskUpdateStatus,
    TaskCommentRead,
    TaskCommentWrite,
    FullTaskRead,
)
from application.task.services import TaskService

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.get("/", status_code=200, response_model=list[TaskRead])
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> list[TaskRead]:
    return await task_service.get_all_tasks()


@task_router.post("/", status_code=201, response_model=TaskRead)
async def create_task(
    task: TaskWrite,
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    return await task_service.create_task(task)


@task_router.patch("/{task_id}/", status_code=200, response_model=TaskRead)
async def update_task_status(
    task_id: int,
    status_info: TaskUpdateStatus,
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    return await task_service.update_task_status(task_id, status_info)


@task_router.get("/{task_id}/", status_code=200, response_model=FullTaskRead)
async def get_full_task_info_by_id(
    task_id: int, task_service: Annotated[TaskService, Depends(get_task_service)]
) -> FullTaskRead:
    return await task_service.get_full_task_info_by_id(task_id)


@task_router.post(
    "/{task_id}/comments/", status_code=201, response_model=TaskCommentRead
)
async def create_task_comment(
    task_id: int,
    comment: TaskCommentWrite,
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskCommentRead:
    return await task_service.create_task_comment(task_id, comment)

