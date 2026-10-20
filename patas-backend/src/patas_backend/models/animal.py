from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


# TODO get from the DB, this is repeated code
class Species(StrEnum):
    CAT = "CAT"
    DOG = "DOG"
    RABBIT = "RABBIT"


@dataclass(frozen=True, slots=True)
class Animal:
    id: UUID
    species: Species
    name: str
    owner_id: UUID

    def __post_init__(self) -> None:
        name = self.name.strip()
        if not name:
            raise ValueError("animal name must not be blank")
        object.__setattr__(self, "name", name)
