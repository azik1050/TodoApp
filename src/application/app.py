from typing import Optional, Self

import uvicorn
from fastapi import FastAPI, APIRouter


class Application:
    __instance: Optional[Self] = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        else:
            raise Exception("This class is already created")

    def __init__(self):
        self._app = FastAPI()

    def __call__(self, *args, **kwargs):
        return self._app

    def create_router(self, prefix: str) -> APIRouter:
        router = APIRouter(prefix=prefix)
        self._app.include_router(router)
        return router


application = Application()

if __name__ == "__main__":
    uvicorn.run(application(), host="0.0.0.0", port=8000)
