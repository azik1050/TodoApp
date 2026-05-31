from _collections_abc import Mapping
from typing import Annotated, Any
from fastapi import HTTPException
from annotated_doc import Doc
from core.utils.schemas.core_schema import CoreSchema


class ResponseError(HTTPException):
    def __init__(
        self,
        status_code: Annotated[
            int,
            Doc(
                """
                HTTP status code to send to the client.

                Read more about it in the
                [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/#use-httpexception)
                """
            ),
        ],
        detail: Annotated[
            Any,
            Doc(
                """
                Any data to be sent to the client in the `detail` key of the JSON
                response.

                Read more about it in the
                [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/#use-httpexception)
                """
            ),
        ] = None,
        headers: Annotated[
            Mapping[str, str] | None,
            Doc(
                """
                Any headers to send to the client in the response.

                Read more about it in the
                [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/#add-custom-headers)

                """
            ),
        ] = None,
    ) -> None:
        """init-override for pydantic model serialization"""

        if isinstance(detail, CoreSchema):
            detail = detail.model_dump(by_alias=True)
        super().__init__(status_code=status_code, detail=detail, headers=headers)