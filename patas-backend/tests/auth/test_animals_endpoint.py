from uuid import uuid4

import httpx
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from patas_backend.models.animal import Animal, AnimalRepository, Species
from patas_backend.models.user import User, UserRepository


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
