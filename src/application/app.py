from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from application.task.routes import task_router
from core.database.base import CoreModel
from core.database.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(CoreModel.metadata.create_all)

    yield

    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
    )
    # routers
    app.include_router(task_router)

    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="127.0.0.1", port=8000)
