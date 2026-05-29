from enum import IntEnum

from pydantic import Field

from src.core.utils.schemas.core_schema import CoreSchema


class TaskPriority(IntEnum):
    HIGH = 3
    MEDIUM = 2
    LOW = 1


class TaskStatus(IntEnum):
    TO_DO = 1
    IN_PROGRESS = 2
    BLOCKED = 3
    CANCELLED = 4
    COMPLETED = 5


class TaskSchema(CoreSchema):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1, max_length=2000)
    priority: TaskPriority
    status: TaskStatus