from uuid import uuid4

import httpx
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from token_issuer import USER_ID, TokenIssuer

from patas_backend.models.animal import Animal, AnimalRepository, Species
from patas_backend.models.user import User, UserRepository


def _bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def _stored_animals(engine: AsyncEngine) -> int:
    async with engine.connect() as conn:
        return await conn.scalar(text("SELECT count(*) FROM patas.animals"))


async def test_catalog_is_public_and_lists_published_animals(
    client: httpx.AsyncClient, engine: AsyncEngine
) -> None:
    # AC5: a visitor without a token sees what was published.
    owner = User.provision(id=uuid4(), name="Ana", email="ana@example.com")
    animal = Animal.publish(
        owner_id=owner.id, name="Milo", species=Species.CAT, age_in_months=14
    )
    async with async_sessionmaker(engine).begin() as session:
        await UserRepository(session).ensure_exists(owner)
        await AnimalRepository(session).add(animal)

    response = await client.get("/animals")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(animal.id),
            "owner_id": str(owner.id),
            "name": "Milo",
            "species": "cat",
            "age_in_months": 14,
            "adoption_status": "available",
        }
    ]


async def test_published_animal_appears_in_the_catalog_owned_by_the_publisher(
    client: httpx.AsyncClient, issuer: TokenIssuer
) -> None:
    # AC1, the vertical slice: HTTP in, row stored, read back through the catalog.
    response = await client.post(
        "/animals",
        json={"name": "  Rex  ", "species": "dog", "age_in_months": 30},
        headers=_bearer(issuer.token()),
    )

    assert response.status_code == 201
    published = response.json()
    assert published["owner_id"] == USER_ID
    assert published["name"] == "Rex"
    assert published["adoption_status"] == "available"
    catalog = (await client.get("/animals")).json()
    assert catalog == [published]


async def test_publishing_without_a_token_is_rejected_and_nothing_is_stored(
    client: httpx.AsyncClient, engine: AsyncEngine
) -> None:
    # AC2
    response = await client.post("/animals", json={"name": "Rex", "species": "dog"})

    assert response.status_code == 401
    assert await _stored_animals(engine) == 0


@pytest.mark.parametrize(
    "body",
    [
        pytest.param({"name": "   ", "species": "dog"}, id="blank-name"),
        pytest.param(
            {"name": "Rex", "species": "dog", "age_in_months": -1}, id="negative-age"
        ),
        pytest.param({"name": "Rex", "species": "rabbit"}, id="unknown-species"),
    ],
)
async def test_invalid_animal_is_rejected_and_nothing_is_stored(
    client: httpx.AsyncClient,
    issuer: TokenIssuer,
    engine: AsyncEngine,
    body: dict[str, object],
) -> None:
    # AC3
    response = await client.post("/animals", json=body, headers=_bearer(issuer.token()))

    assert response.status_code == 422
    assert await _stored_animals(engine) == 0
