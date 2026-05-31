import asyncio

import pytest
from fastapi.testclient import TestClient

from src.application.app import create_app
from src.core.database.base import CoreModel
from src.core.database.session import engine


@pytest.fixture(scope="session")
def client():
    with TestClient(create_app()) as client:
        yield client


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
