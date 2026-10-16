from collections.abc import Mapping
from dataclasses import dataclass
from uuid import UUID

from patas_backend.models.user import InvalidUser, validate_email, validate_name


class InvalidClaims(ValueError):
    """The token claims do not describe a valid user."""


@dataclass(frozen=True, slots=True)
class AuthenticatedPrincipal:
    """Who the verified token says is calling. Built only from validated claims."""

    id: UUID
    email: str
    name: str

    def __post_init__(self) -> None:
        try:
            # Frozen dataclass: object.__setattr__ stores the trimmed values once.
            object.__setattr__(self, "name", validate_name(self.name))
            object.__setattr__(self, "email", validate_email(self.email))
        except InvalidUser as error:
            raise InvalidClaims(str(error)) from error

    @classmethod
    def from_claims(cls, claims: Mapping[str, object]) -> "AuthenticatedPrincipal":
        return cls(
            id=_uuid(claims.get("sub")),
            email=_text(claims, "email"),
            name=_text(claims, "name"),
        )


def _text(claims: Mapping[str, object], key: str) -> str:
    value = claims.get(key)
    if not isinstance(value, str):
        raise InvalidClaims(f"claim '{key}' must be a string")
    return value


def _uuid(value: object) -> UUID:
    if not isinstance(value, str):
        raise InvalidClaims("claim 'sub' must be a string")
    try:
        return UUID(value)
    except ValueError as error:
        raise InvalidClaims("claim 'sub' must be a UUID") from error
