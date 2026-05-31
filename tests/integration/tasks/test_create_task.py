import pytest

from src.application.task.schemas import TaskWrite, TaskPriority


@pytest.mark.integration
def test_create_task(client):
    task = TaskWrite(
        title="Hello World",
        content="Hello World",
        priority=TaskPriority.MEDIUM,
    )
    response = client.post("/tasks", json=task.model_dump(by_alias=True))
    assert response.status_code == 201
