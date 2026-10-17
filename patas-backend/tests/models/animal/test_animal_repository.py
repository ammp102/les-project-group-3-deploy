from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from patas_backend.models.animal import (
    AdoptionStatus,
    Animal,
    AnimalRepository,
    Species,
)
from patas_backend.models.user import User, UserRepository

ANA_ID = UUID("0b1f2a3c-4d5e-4f60-8a7b-9c0d1e2f3a4b")
BOB_ID = UUID("5c6d7e8f-9a0b-4c1d-8e2f-3a4b5c6d7e8f")

Factory = async_sessionmaker[AsyncSession]


async def _provision(factory: Factory, user_id: UUID, email: str) -> UUID:
    async with factory.begin() as session:
        await UserRepository(session).ensure_exists(
            User.provision(id=user_id, name="Owner", email=email)
        )
    return user_id


@pytest_asyncio.fixture
async def ana(session_factory: Factory) -> UUID:
    return await _provision(session_factory, ANA_ID, "ana@example.com")


def _publish(owner_id: UUID, **overrides: object) -> Animal:
    return Animal.publish(
        **{
            "owner_id": owner_id,
            "name": "Rex",
            "species": Species.DOG,
            "age_in_months": 12,
            **overrides,
        }
    )


async def _add(factory: Factory, animal: Animal) -> None:
    async with factory.begin() as session:
        await AnimalRepository(session).add(animal)


async def _list(factory: Factory) -> list[Animal]:
    async with factory() as session:
        return await AnimalRepository(session).list_all()


async def test_the_catalog_is_empty_before_anything_is_published(
    session_factory: Factory,
) -> None:
    assert await _list(session_factory) == []


@pytest.mark.parametrize("species", list(Species))
async def test_a_published_animal_is_listed_with_its_owner(
    session_factory: Factory, ana: UUID, species: Species
) -> None:
    animal = _publish(ana, species=species)

    await _add(session_factory, animal)

    listed = await _list(session_factory)
    assert listed == [animal]
    assert listed[0].owner_id == ana
    assert listed[0].adoption_status is AdoptionStatus.AVAILABLE


async def test_an_animal_of_unknown_age_round_trips(
    session_factory: Factory, ana: UUID
) -> None:
    animal = _publish(ana, age_in_months=None)

    await _add(session_factory, animal)

    assert await _list(session_factory) == [animal]


@pytest.mark.parametrize("status", list(AdoptionStatus))
async def test_the_stored_adoption_status_is_loaded(
    session_factory: Factory, ana: UUID, status: AdoptionStatus
) -> None:
    animal = Animal(
        id=uuid4(),
        owner_id=ana,
        name="Rex",
        species=Species.DOG,
        adoption_status=status,
    )

    await _add(session_factory, animal)

    assert (await _list(session_factory))[0].adoption_status is status


async def test_the_catalog_lists_the_newest_animal_first(
    session_factory: Factory, ana: UUID
) -> None:
    await _add(session_factory, _publish(ana, name="Rex"))
    await _add(session_factory, _publish(ana, name="Luna"))

    assert [a.name for a in await _list(session_factory)] == ["Luna", "Rex"]


async def test_the_catalog_lists_the_animals_of_every_owner(
    session_factory: Factory, ana: UUID
) -> None:
    bob = await _provision(session_factory, BOB_ID, "bob@example.com")
    await _add(session_factory, _publish(ana, name="Rex"))
    await _add(session_factory, _publish(bob, name="Luna"))

    owners = {a.name: a.owner_id for a in await _list(session_factory)}

    assert owners == {"Rex": ana, "Luna": bob}


async def test_add_never_commits_so_the_caller_can_roll_back(
    session_factory: Factory, ana: UUID
) -> None:
    async with session_factory() as session:
        await AnimalRepository(session).add(_publish(ana))
        await session.rollback()

    assert await _list(session_factory) == []
