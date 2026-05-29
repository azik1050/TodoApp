from sqlalchemy import Integer, String, DateTime

from src.application.tasks.schemas import TaskPriority, TaskStatus
from src.core.database.base import CoreModel
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime


class TaskModel(CoreModel):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(String(2000))
    priority: Mapped[TaskPriority] = mapped_column(Integer)
    status: Mapped[TaskStatus] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default_factory=datetime.now)
