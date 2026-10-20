from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from patas_backend.models.animal.animal import AdoptionStatus, Animal, Species

_INSERT = text(
    """
    INSERT INTO patas.animals
        (id, owner_id, name, species, age_in_months, adoption_status)
    VALUES (
        :id, :owner_id, :name, CAST(:species AS patas.species), :age_in_months,
        CAST(:adoption_status AS patas.adoption_status)
    )
    """
)
# created_at ties only inside one transaction (now() is fixed per transaction), so
# id keeps the order deterministic there.
_SELECT_ALL = text(
    """
    SELECT id, owner_id, name, species, age_in_months, adoption_status
    FROM patas.animals
    ORDER BY created_at DESC, id
    """
)


class AnimalRepository:
    """Persistence for Animal. The caller owns the transaction (this never commits)."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, animal: Animal) -> None:
        await self._session.execute(
            _INSERT,
            {
                "id": animal.id,
                "owner_id": animal.owner_id,
                "name": animal.name,
                "species": animal.species.value,
                "age_in_months": animal.age_in_months,
                "adoption_status": animal.adoption_status.value,
            },
        )

    async def list_all(self) -> list[Animal]:
        """Every animal of every owner, newest first: the public catalog."""
        result = await self._session.execute(_SELECT_ALL)
        return [
            Animal(
                id=row.id,
                owner_id=row.owner_id,
                name=row.name,
                species=Species(row.species),
                age_in_months=row.age_in_months,
                adoption_status=AdoptionStatus(row.adoption_status),
            )
            for row in result
        ]
