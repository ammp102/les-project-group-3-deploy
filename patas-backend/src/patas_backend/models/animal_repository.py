from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from patas_backend.models.animal import Animal, Species

_SELECT_ANIMALS = text(
    """
    SELECT id, species, name, owner_id
    FROM patas.animal
    ORDER BY name, id
    """
)


class AnimalRepository:
    """Read animal records from the database."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Animal]:
        rows = (await self._session.execute(_SELECT_ANIMALS)).all()
        return [
            Animal(
                id=row.id,
                species=Species(row.species),
                name=row.name,
                owner_id=row.owner_id,
            )
            for row in rows
        ]
