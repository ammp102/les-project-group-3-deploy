from typing import Annotated

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PATAS_", env_file=".env")

    # Default points at the local docker-compose database, which has no TLS.
    database_url: Annotated[
        str,
        Field(validation_alias=AliasChoices("DATABASE_URL", "PATAS_DATABASE_URL")),
    ] = (
        "postgresql+asyncpg://patas_admin:securepassword@localhost:5433/patas_db"
        "?ssl=disable"
    )
    jwks_url: str = "http://localhost:3000/api/auth/jwks"
    jwt_issuer: str = "http://localhost:3000"
    jwt_audience: str = "http://localhost:3000"
