import pytest

from application.task.schemas import TaskWrite, TaskPriority


@pytest.fixture(scope="function")
def task(client):
    return client.post(
        "/tasks",
        json=TaskWrite(
            title="Test Task",
            content="This is a test task.",
            priority=TaskPriority.MEDIUM,
        ).model_dump(by_alias=True),
    )