from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CoreSchema(BaseModel):
    model_config = ConfigDict(
        strict=True,
        extra="forbid",
        populate_by_name=True,
        use_enum_values=True,
        alias_generator=to_camel,
        validation_error_cause=True,
    )

