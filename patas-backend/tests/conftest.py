import asyncio
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
import pytest_asyncio
from alembic.config import Config
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from alembic import command
from patas_backend.config import Settings

TEST_DATABASE = "patas_test"
ALEMBIC_INI = Path(__file__).resolve().parents[1] / "alembic.ini"


def _test_database_url() -> str:
    url = make_url(Settings().database_url)
    return url.set(database=TEST_DATABASE).render_as_string(hide_password=False)


async def _create_test_database_if_missing() -> None:
    admin = create_async_engine(Settings().database_url, isolation_level="AUTOCOMMIT")
    async with admin.connect() as conn:
        exists = await conn.scalar(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": TEST_DATABASE},
        )
        if not exists:
            await conn.execute(text(f"CREATE DATABASE {TEST_DATABASE}"))
    await admin.dispose()


async def _drop_domain_schema(url: str) -> None:
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA IF EXISTS patas CASCADE"))
        await conn.execute(text("DROP SCHEMA IF EXISTS patas_auth CASCADE"))
    await engine.dispose()


@pytest.fixture(scope="session")
def migrated_database_url() -> str:
    """A real PostgreSQL database with every migration applied from scratch."""
    url = _test_database_url()
    asyncio.run(_create_test_database_if_missing())
    asyncio.run(_drop_domain_schema(url))

    config = Config(str(ALEMBIC_INI))
    config.set_main_option("sqlalchemy.url", url)
    command.upgrade(config, "head")
    return url


@pytest_asyncio.fixture
async def engine(migrated_database_url: str) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(migrated_database_url)
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE patas.users CASCADE"))
    yield engine
    await engine.dispose()
