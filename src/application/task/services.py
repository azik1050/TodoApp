import asyncio
from application.task.schemas import TaskCommentWrite, FullTaskRead
from typing import Optional, Annotated

from fastapi import Depends

from application.shared.dependencies.mappers import get_task_service_mapper
from application.shared.dependencies.repos import (
    get_task_repo,
    get_task_comment_repo,
    get_task_status_history_repo,
)
from application.task.mappers import TaskServiceMapper
from application.task.models import TaskModel, TaskCommentModel, TaskStatusHistoryModel
from application.task.repositories import (
    TaskRepo,
    TaskCommentRepo,
    TaskStatusHistoryRepo,
)
from src.application.task.schemas import (
    TaskWrite,
    TaskRead,
    TaskStatus,
    TaskUpdateStatus,
)
from core.utils.exceptions.service_exceptions import (
    RecordNotFound,
    RecordAlreadyExists,
    ServerError,
    RuleViolation,
)


class TaskService:
    def __init__(
        self,
        task_repo: Annotated[TaskRepo, Depends(get_task_repo)],
        task_comment_repo: Annotated[TaskCommentRepo, Depends(get_task_comment_repo)],
        task_status_history_repo: Annotated[
            TaskStatusHistoryRepo, Depends(get_task_status_history_repo)
        ],
        task_service_mapper: Annotated[
            TaskServiceMapper, Depends(get_task_service_mapper)
        ],
    ) -> None:
        # repos
        self._task_repo = task_repo
        self._task_comment_repo = task_comment_repo
        self._task_status_history_repo = task_status_history_repo
        # mapper
        self._task_service_mapper = task_service_mapper

    async def get_all_tasks(self) -> list[TaskRead]:
        tasks = await self._task_repo.get_all()
        if len(tasks) == 0:
            raise RecordNotFound("Tasks could not be found")
        return self._task_service_mapper.get_all_tasks(tasks)

    async def create_task(self, task: TaskWrite) -> TaskRead:
        try:
            created_task = await self._task_repo.create(
                TaskModel(
                    title=task.title,
                    content=task.content,
                    status=TaskStatus.TO_DO,
                    priority=task.priority,
                )
            )
        except Exception:
            raise RecordAlreadyExists("Task already exists")
        return self._task_service_mapper.create_task(created_task)

    async def update_task_status(
        self, task_id: int, new_status_info: TaskUpdateStatus
    ) -> TaskRead:
        ALLOWED_STATUSES = {
            TaskStatus.TO_DO: (
                TaskStatus.BLOCKED,
                TaskStatus.CANCELLED,
                TaskStatus.IN_PROGRESS,
            ),
            TaskStatus.IN_PROGRESS: (
                TaskStatus.BLOCKED,
                TaskStatus.CANCELLED,
                TaskStatus.TO_DO,
                TaskStatus.COMPLETED,
            ),
            TaskStatus.COMPLETED: (),
            TaskStatus.CANCELLED: (),
            TaskStatus.BLOCKED: (
                TaskStatus.CANCELLED,
                TaskStatus.IN_PROGRESS,
                TaskStatus.TO_DO,
            ),
        }

        try:
            target_task: Optional[TaskModel] = await self._task_repo.get_by_pk(task_id)
            if not target_task:
                raise RecordNotFound("Task could not be found")

            if new_status_info.status in ALLOWED_STATUSES[target_task.status]:
                # If current task status is 'BLOCKED', check that it is rolled back to a previous status
                if target_task.status == TaskStatus.BLOCKED:
                    task_previous_status_info = await self._task_status_history_repo.get_previous_task_status_by_task_id(
                        task_id
                    )
                    if task_previous_status_info.old_status != new_status_info.status:
                        raise RuleViolation(
                            f"Task can only be changed to the previous status: '{task_previous_status_info.old_status}'"
                        )

                # Save old status for logging change in DB
                old_status = target_task.status
                # Update task status
                target_task.status = new_status_info.status
                updated_task = await self._task_repo.update(target_task)
                # Save change of status in DB
                await self._task_status_history_repo.create(
                    TaskStatusHistoryModel(
                        task_id=task_id,
                        new_status=new_status_info.status,
                        old_status=old_status,
                    )
                )
            else:
                raise RuleViolation(
                    f"Status cannot be changed from '{new_status_info.status}' to '{target_task.status}'"
                )
        except RecordNotFound, RuleViolation:
            raise
        except Exception as e:
            raise ServerError(e)

        return self._task_service_mapper.update_task_status(updated_task)

    async def get_full_task_info_by_id(self, task_id: int) -> FullTaskRead:
        try:
            task = await self._task_repo.get_by_pk(task_id)
            if not task:
                raise RecordNotFound("Task could not be found")

            task_status_history, task_comments = await asyncio.gather(
                self._task_status_history_repo.get_by_task_id(task_id),
                self._task_comment_repo.get_by_task_id(task_id),
            )
        except RecordNotFound:
            raise
        return self._task_service_mapper.get_full_task_info(
            task, task_status_history, task_comments
        )

    async def create_task_comment(
        self, task_id: int, comment: TaskCommentWrite
    ) -> TaskRead:
        try:
            task = await self._task_repo.get_by_pk(task_id)
            if not task:
                raise RecordNotFound("Task could not be found")

            task_comment = await self._task_comment_repo.create(
                TaskCommentModel(
                    text=comment.text,
                    task_id=task_id,
                )
            )
        except RecordNotFound, RuleViolation:
            raise
        return self._task_service_mapper.create_task_comment(task_comment)