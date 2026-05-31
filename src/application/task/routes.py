from fastapi import APIRouter
from fastapi.params import Depends
from typing import Annotated

from application.shared.dependencies.services import get_task_service
from application.shared.contracts.schemas import ErrorSchema
from application.task.schemas import (
    TaskWrite,
    TaskRead,
    TaskUpdateStatus,
    TaskCommentRead,
    TaskCommentWrite,
    FullTaskRead,
)
from application.task.services import TaskService
from core.utils.exceptions.response_error import ResponseError
from core.utils.exceptions.service_exceptions import (
    RecordNotFound,
    RecordAlreadyExists,
    ServerError,
    RuleViolation,
)

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.get("/", status_code=200, response_model=list[TaskRead])
async def get_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> list[TaskRead]:
    try:
        response = await task_service.get_all_tasks()
    except RecordNotFound as e:
        raise ResponseError(status_code=404, detail=ErrorSchema(text=str(e)))
    return response


@task_router.post("/", status_code=201, response_model=TaskRead)
async def create_task(
    task: TaskWrite,
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    try:
        response = await task_service.create_task(task)
    except RecordAlreadyExists as e:
        raise ResponseError(status_code=400, detail=ErrorSchema(text=str(e)))
    return response


@task_router.patch("/{task_id}/", status_code=200, response_model=TaskRead)
async def update_task_status(
    task_id: int,
    status_info: TaskUpdateStatus,
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskRead:
    try:
        response = await task_service.update_task_status(task_id, status_info)
    except RecordNotFound as e:
        raise ResponseError(status_code=404, detail=ErrorSchema(text=str(e)))
    except RuleViolation as e:
        raise ResponseError(status_code=422, detail=ErrorSchema(text=str(e)))
    except ServerError as e:
        raise ResponseError(status_code=500, detail=ErrorSchema(text=str(e)))
    return response


@task_router.get("/{task_id}/", status_code=200, response_model=FullTaskRead)
async def get_full_task_info_by_id(
    task_id: int, task_service: Annotated[TaskService, Depends(get_task_service)]
) -> FullTaskRead:
    try:
        response = await task_service.get_full_task_info_by_id(task_id)
    except RecordNotFound as e:
        raise ResponseError(status_code=404, detail=ErrorSchema(text=str(e)))
    print(response.model_dump(by_alias=True))
    return response


@task_router.post(
    "/{task_id}/comments/", status_code=201, response_model=TaskCommentRead
)
async def create_task_comment(
    task_id: int,
    comment: TaskCommentWrite,
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskCommentRead:
    try:
        response = await task_service.create_task_comment(task_id, comment)
    except RecordAlreadyExists as e:
        raise ResponseError(status_code=409, detail=ErrorSchema(text=str(e)))
    except RecordNotFound as e:
        raise ResponseError(status_code=404, detail=ErrorSchema(text=str(e)))
    return response

