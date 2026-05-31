from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PgConfig(BaseSettings):
    username: str
    password: SecretStr
    host: str
    port: int
    dbname: str

    model_config = SettingsConfigDict(
        env_prefix="PG.", case_sensitive=True, env_nested_delimiter=".", extra="forbid"
    )


db_settings = PgConfig()