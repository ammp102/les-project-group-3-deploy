from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel

from patas_backend.auth.dependencies import get_current_user
from patas_backend.models.animal import (
    AdoptionStatus,
    Animal,
    InvalidAnimal,
    Species,
)
from patas_backend.models.user import User
from patas_backend.services.animals import AnimalService

router = APIRouter()


class PublishAnimalRequest(BaseModel):
    # Types only. The business rules (non-blank name, age >= 0) live in the domain.
    name: str
    species: Species
    age_in_months: int | None = None


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


def get_animal_service(request: Request) -> AnimalService:
    return AnimalService(request.app.state.session_factory)


@router.get("/animals", response_model=list[AnimalResponse])
async def list_animals(
    service: Annotated[AnimalService, Depends(get_animal_service)],
) -> list[AnimalResponse]:
    """The public catalog: no authentication dependency (AC5)."""
    return [AnimalResponse.from_domain(a) for a in await service.list_catalog()]


@router.post(
    "/animals", status_code=status.HTTP_201_CREATED, response_model=AnimalResponse
)
async def publish_animal(
    body: PublishAnimalRequest,
    owner: Annotated[User, Depends(get_current_user)],
    service: Annotated[AnimalService, Depends(get_animal_service)],
) -> AnimalResponse:
    try:
        animal = await service.publish(
            owner,
            name=body.name,
            species=body.species,
            age_in_months=body.age_in_months,
        )
    except InvalidAnimal as error:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT, str(error)
        ) from error
    return AnimalResponse.from_domain(animal)
