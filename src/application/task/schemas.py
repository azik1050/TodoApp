from enum import StrEnum
from typing import Optional
from datetime import datetime

from pydantic import Field

from core.utils.schemas.core_schema import CoreSchema


class TaskPriority(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class TaskStatus(StrEnum):
    TO_DO = "TO_DO"
    IN_PROGRESS = "IN_PROGRESS"
    BLOCKED = "BLOCKED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


# Task Response Models
class TaskBase(CoreSchema):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=2000)
    priority: TaskPriority = Field(strict=False)


class TaskRead(TaskBase):
    id: Optional[int] = Field(default=None)
    status: TaskStatus = Field(strict=False)


class TaskWrite(TaskBase):
    pass


class TaskUpdateStatus(CoreSchema):
    status: TaskStatus = Field(strict=False)


# Task-Comment Response Models
class TaskCommentRead(CoreSchema):
    id: int
    text: str = Field(..., min_length=1, max_length=500)
    created_at: datetime


class TaskCommentWrite(CoreSchema):
    text: str = Field(..., min_length=1, max_length=500)


# Task-History Response Models
class TaskStatusHistoryRead(CoreSchema):
    new_status: TaskStatus = Field(strict=False)
    old_status: TaskStatus = Field(strict=False)
    created_at: datetime


# Full Task Response Model
class FullTaskRead(CoreSchema):
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=2000)
    priority: TaskPriority = Field(strict=False)
    status: TaskStatus = Field(strict=False)
    history: list[TaskStatusHistoryRead]
    comments: list[TaskCommentRead]