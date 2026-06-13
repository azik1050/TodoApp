from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from application.shared.contracts.schemas import ErrorSchema
from core.utils.exceptions.service_exceptions import (
    BaseServiceException,
    RecordNotFound,
    RecordAlreadyExists,
    RuleViolation,
)


class ExceptionHandler:
    def __init__(self, app: FastAPI) -> None:
        app.add_exception_handler(RecordNotFound, self.handle_exception)
        app.add_exception_handler(RecordAlreadyExists, self.handle_exception)
        app.add_exception_handler(RuleViolation, self.handle_exception)

    @staticmethod
    def handle_exception(
        request: Request, exception: BaseServiceException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exception.status_code,
            content=ErrorSchema(error_text=str(exception)).model_dump(by_alias=True),
        )

