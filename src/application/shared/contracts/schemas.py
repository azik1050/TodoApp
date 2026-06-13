from pydantic import field_validator

from core.utils.schemas.core_schema import CoreSchema


class ErrorSchema(CoreSchema):
    """
    Schema for representing error responses in the application.
    Attributes:
        error_text (str): A string describing the error details.
    """

    error_text: str

    @field_validator("error_text", mode="before")
    @classmethod
    def convert_error_to_str(cls, value):
        return str(value)