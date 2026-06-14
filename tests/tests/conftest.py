import asyncio

import pytest
from fastapi.testclient import TestClient

from src.application.app import create_app
from src.core.database.base import CoreModel
from src.core.database.session import engine
from tests.application.clients.task_client import TaskClient

# Pydantic schemas used in fixtures
from src.application.task.schemas import TaskWrite, TaskPriority, TaskRead


@pytest.fixture(scope="session")
def test_client():
    with TestClient(create_app()) as client:
        yield client


@pytest.fixture(scope="session")
def task_client(test_client) -> TaskClient:
    return TaskClient(test_client)


# Provide an alias `client` used by some tests
@pytest.fixture(scope="session")
def client(test_client):
    return test_client


@pytest.fixture
def task(task_client) -> TaskRead:
    """Create a task and return a validated TaskRead model instance."""
    task = TaskWrite(title="Test Task", content="This is a test task.", priority=TaskPriority.MEDIUM)
    response = task_client.create_task(task.model_dump(by_alias=True))
    assert response.status_code == 201
    return TaskRead.model_validate(response.json())


@pytest.fixture(autouse=True)
def clean_database():
    async def cleanup():
        async with engine.begin() as connection:
            await connection.run_sync(CoreModel.metadata.create_all)
            for table in reversed(CoreModel.metadata.sorted_tables):
                await connection.execute(table.delete())

    asyncio.run(cleanup())
    yield
    asyncio.run(cleanup())
