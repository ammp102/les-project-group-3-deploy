from uuid import UUID, uuid4

import pytest

from patas_backend.models.animal import AdoptionStatus, Animal, InvalidAnimal, Species

OWNER_ID = UUID("0b1f2a3c-4d5e-4f60-8a7b-9c0d1e2f3a4b")


def _publish(**overrides: object) -> Animal:
    return Animal.publish(
        **{
            "owner_id": OWNER_ID,
            "name": "Rex",
            "species": Species.DOG,
            "age_in_months": 12,
            **overrides,
        }
    )


def test_a_published_animal_is_available_and_owned_by_the_publisher() -> None:
    animal = _publish()

    assert animal.owner_id == OWNER_ID
    assert animal.adoption_status is AdoptionStatus.AVAILABLE


def test_each_published_animal_gets_its_own_id() -> None:
    assert _publish().id != _publish().id


def test_name_is_trimmed() -> None:
    assert _publish(name="  Rex  ").name == "Rex"


@pytest.mark.parametrize("name", ["", "   "])
def test_blank_name_is_rejected(name: str) -> None:
    with pytest.raises(InvalidAnimal):
        _publish(name=name)


def test_negative_age_is_rejected() -> None:
    with pytest.raises(InvalidAnimal):
        _publish(age_in_months=-1)


def test_a_newborn_of_zero_months_is_accepted() -> None:
    assert _publish(age_in_months=0).age_in_months == 0


def test_age_is_optional() -> None:
    assert _publish(age_in_months=None).age_in_months is None


def test_invariants_hold_when_built_directly() -> None:
    # Loading from the database goes through the constructor, not `publish`.
    with pytest.raises(InvalidAnimal):
        Animal(id=uuid4(), owner_id=OWNER_ID, name=" ", species=Species.DOG)
