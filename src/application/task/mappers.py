from application.task.models import TaskModel, TaskCommentModel, TaskStatusHistoryModel
from application.task.schemas import (
    TaskRead,
    TaskCommentRead,
    FullTaskRead,
    TaskStatusHistoryRead,
)


class TaskServiceMapper:
    @staticmethod
    def get_all_tasks(tasks: list[TaskModel]) -> list[TaskRead]:
        return [
            TaskRead(
                id=task.id,
                title=task.title,
                content=task.content,
                status=task.status,
                priority=task.priority,
            )
            for task in tasks
        ]

    @staticmethod
    def create_task(task: TaskModel) -> TaskRead:
        return TaskRead(
            id=task.id,
            title=task.title,
            content=task.content,
            status=task.status,
            priority=task.priority,
        )

    @staticmethod
    def update_task_status(task: TaskModel) -> TaskRead:
        return TaskRead(
            id=task.id,
            title=task.title,
            content=task.content,
            status=task.status,
            priority=task.priority,
        )

    @staticmethod
    def get_full_task_info(
        task: TaskModel,
        task_status_history: list[TaskStatusHistoryModel],
        task_comments: list[TaskCommentModel],
    ) -> FullTaskRead:
        return FullTaskRead(
            id=task.id,
            title=task.title,
            content=task.content,
            status=task.status,
            priority=task.priority,
            history=[
                TaskStatusHistoryRead(
                    new_status=status_change.new_status,
                    old_status=status_change.old_status,
                    created_at=status_change.created_at,
                )
                for status_change in task_status_history
            ],
            comments=[
                TaskCommentRead(
                    id=comment.id,
                    text=comment.text,
                    created_at=comment.created_at,
                )
                for comment in task_comments
            ],
        )

    @staticmethod
    def create_task_comment(task_comment: TaskCommentModel) -> TaskCommentRead:
        return TaskCommentRead(
            id=task_comment.id,
            text=task_comment.text,
            created_at=task_comment.created_at,
        )