import pytest

from src.application.task.schemas import TaskWrite, TaskPriority


@pytest.mark.integration
def test_create_task(task_client):
    task = TaskWrite(
        title="Hello World",
        content="Hello World",
        priority=TaskPriority.MEDIUM,
    )
    response = task_client.create_task(task.model_dump(by_alias=True))
    assert response.status_code == 201
