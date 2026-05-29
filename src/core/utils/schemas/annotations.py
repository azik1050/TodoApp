from pydantic import Field
from sqlalchemy.sql.annotation import Annotated

NonEmptyStr = Annotated[str, Field(min_length=1)]