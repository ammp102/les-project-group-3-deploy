from collections.abc import AsyncIterator
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from patas_backend.models.animal import (
    AdoptionStatus,
    Animal,
    AnimalRepository,
    Species,
)

router = APIRouter()


class AnimalResponse(BaseModel):
    id: UUID
    owner_id: UUID
    name: str
    species: Species
    age_in_months: int | None
    adoption_status: AdoptionStatus

    @classmethod
    def from_domain(cls, animal: Animal) -> "AnimalResponse":
        return cls(
            id=animal.id,
            owner_id=animal.owner_id,
            name=animal.name,
            species=animal.species,
            age_in_months=animal.age_in_months,
            adoption_status=animal.adoption_status,
        )


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with request.app.state.session_factory() as session:
        yield session


@router.get("/animals", response_model=list[AnimalResponse])
async def list_animals(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[AnimalResponse]:
    """The public catalog: no authentication dependency (AC5)."""
    animals = await AnimalRepository(session).list_all()
    return [AnimalResponse.from_domain(animal) for animal in animals]
