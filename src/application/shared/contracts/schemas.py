from core.utils.schemas.core_schema import CoreSchema


class ErrorSchema(CoreSchema):
    """
    Schema for representing error responses in the application.
    Attributes:
        text (str): A string describing the error details.
    """
    text: str
