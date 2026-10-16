from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PATAS_", env_file=".env")

    # Default points at the local docker-compose database, which has no TLS.
    database_url: str = (
        "postgresql+asyncpg://patas_admin:securepassword@localhost:5433/patas_db"
        "?ssl=disable"
    )
    jwks_url: str = "http://localhost:3000/api/auth/jwks"
    jwt_issuer: str = "http://localhost:3000"
    jwt_audience: str = "http://localhost:3000"
