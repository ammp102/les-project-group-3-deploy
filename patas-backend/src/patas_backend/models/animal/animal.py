from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID, uuid4


class InvalidAnimal(ValueError):
    """An Animal invariant was violated."""


class Species(StrEnum):
    DOG = "dog"
    CAT = "cat"
    OTHER = "other"


class AdoptionStatus(StrEnum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    IN_TRIAL = "in_trial"
    ADOPTED = "adopted"
    UNAVAILABLE = "unavailable"


def validate_name(name: str) -> str:
    cleaned = name.strip()
    if not cleaned:
        raise InvalidAnimal("name must not be blank")
    return cleaned


def validate_age_in_months(age_in_months: int | None) -> int | None:
    if age_in_months is not None and age_in_months < 0:
        raise InvalidAnimal("age must not be negative")
    return age_in_months


@dataclass
class Animal:
    id: UUID
    owner_id: UUID
    name: str
    species: Species
    age_in_months: int | None = None
    adoption_status: AdoptionStatus = AdoptionStatus.AVAILABLE

    def __post_init__(self) -> None:
        # Invariants hold however an Animal is built (published or loaded from the DB).
        self.name = validate_name(self.name)
        self.age_in_months = validate_age_in_months(self.age_in_months)

    @classmethod
    def publish(
        cls,
        *,
        owner_id: UUID,
        name: str,
        species: Species,
        age_in_months: int | None = None,
    ) -> "Animal":
        """Create a new listing. It always starts available, owned by its publisher."""
        return cls(
            id=uuid4(),
            owner_id=owner_id,
            name=name,
            species=species,
            age_in_months=age_in_months,
        )
