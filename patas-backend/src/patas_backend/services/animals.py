from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from patas_backend.models.animal import Animal, AnimalRepository, Species
from patas_backend.models.user import User


class AnimalService:
    """Animal use cases. Each one owns its transaction."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def publish(
        self,
        owner: User,
        *,
        name: str,
        species: Species,
        age_in_months: int | None,
    ) -> Animal:
        """A1 (create): the logged-in user publishes an animal they own."""
        # Built before the transaction opens: an invalid animal raises InvalidAnimal
        # and nothing reaches the database (AC3).
        animal = Animal.publish(
            owner_id=owner.id, name=name, species=species, age_in_months=age_in_months
        )
        async with self._session_factory.begin() as session:
            await AnimalRepository(session).add(animal)
        return animal

    async def list_catalog(self) -> list[Animal]:
        """A2 (list): every published animal, newest first. Public."""
        # Read-only: a plain session, no transaction to commit.
        async with self._session_factory() as session:
            return await AnimalRepository(session).list_all()
