from sqlalchemy import Integer, String, DateTime, func, ForeignKey

from application.task.schemas import TaskPriority, TaskStatus
from core.database.base import CoreModel
from sqlalchemy.orm import mapped_column, Mapped, relationship
from datetime import datetime


class TaskModel(CoreModel):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(2000))
    priority: Mapped[TaskPriority] = mapped_column(String(50))
    status: Mapped[TaskStatus] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # ORM Relations with other models
    comments: Mapped["TaskCommentModel"] = relationship(
        "TaskCommentModel", back_populates="task"
    )
    status_history: Mapped["TaskStatusHistoryModel"] = relationship(
        "TaskStatusHistoryModel", back_populates="task"
    )


class TaskCommentModel(CoreModel):
    __tablename__ = "task_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    text: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # ORM Relations with other models
    task: Mapped["TaskModel"] = relationship("TaskModel", back_populates="comments")


class TaskStatusHistoryModel(CoreModel):
    __tablename__ = "task_status_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    new_status: Mapped[str] = mapped_column(String(50))
    old_status: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # ORM Relations with other models
    task: Mapped["TaskModel"] = relationship(
        "TaskModel", back_populates="status_history"
    )
