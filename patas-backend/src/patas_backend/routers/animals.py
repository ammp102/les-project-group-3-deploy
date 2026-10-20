from collections.abc import AsyncIterator
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from patas_backend.models.animal import Species
from patas_backend.models.animal_repository import AnimalRepository

router = APIRouter()


class AnimalResponse(BaseModel):
    id: UUID
    species: Species
    name: str
    owner_id: UUID


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with request.app.state.session_factory() as session:
        yield session


@router.get("/animals", response_model=list[AnimalResponse])
async def list_animals(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[AnimalResponse]:
    animals = await AnimalRepository(session).list_all()
    return [
        AnimalResponse(
            id=animal.id,
            species=animal.species,
            name=animal.name,
            owner_id=animal.owner_id,
        )
        for animal in animals
    ]
