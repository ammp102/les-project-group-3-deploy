import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


async def test_animals_endpoint_returns_seeded_animals(
    client: httpx.AsyncClient, engine: AsyncEngine
) -> None:
    response = await client.get("/animals")

    assert response.status_code == 200
    animals = response.json()
    assert len(animals) == 6
    assert {animal["species"] for animal in animals} == {"CAT", "DOG", "RABBIT"}
    assert {animal["name"] for animal in animals} == {
        "Milo",
        "Luna",
        "Pipoca",
        "Nina",
        "Bobby",
        "Cenoura",
    }
    assert all(animal["id"] and animal["owner_id"] for animal in animals)
    async with engine.connect() as connection:
        foreign_keys = await connection.scalar(
            text(
                """
                SELECT count(*)
                FROM information_schema.table_constraints
                WHERE table_schema = 'patas'
                  AND table_name = 'animal'
                  AND constraint_type = 'FOREIGN KEY'
                """
            )
        )
    assert foreign_keys == 0
