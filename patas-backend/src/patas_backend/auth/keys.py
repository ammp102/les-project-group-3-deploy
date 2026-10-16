from abc import ABC, abstractmethod
from collections.abc import Mapping

import jwt
from jwt import PyJWK, PyJWKClient, PyJWKSet
from jwt.exceptions import PyJWKClientConnectionError, PyJWKClientError, PyJWKSetError

from patas_backend.auth.errors import InvalidToken, KeysUnavailable, UnknownSigningKey


class JwksKeyProvider(ABC):
    """Supplies the public key that must have signed a given token."""

    @abstractmethod
    def signing_key_for(self, token: str) -> PyJWK: ...


def _key_id(token: str) -> str:
    try:
        key_id = jwt.get_unverified_header(token).get("kid")
    except jwt.PyJWTError as error:
        raise InvalidToken("malformed token") from error
    if not isinstance(key_id, str):
        raise InvalidToken("token has no key id")
    return key_id


class StaticJwksKeyProvider(JwksKeyProvider):
    """A fixed key set. Used by tests, so the signature check itself stays real."""

    def __init__(self, jwks: Mapping[str, object]) -> None:
        self._keys = {key.key_id: key for key in PyJWKSet.from_dict(dict(jwks)).keys}

    def signing_key_for(self, token: str) -> PyJWK:
        key_id = _key_id(token)
        try:
            return self._keys[key_id]
        except KeyError as error:
            raise UnknownSigningKey(f"unknown key id '{key_id}'") from error


class RemoteJwksKeyProvider(JwksKeyProvider):
    """Fetches the keys from the Better-Auth JWKS endpoint (cached by PyJWKClient)."""

    def __init__(self, url: str, *, timeout: float = 5) -> None:
        self._client = PyJWKClient(url, timeout=timeout)

    def signing_key_for(self, token: str) -> PyJWK:
        try:
            return self._client.get_signing_key_from_jwt(token)
        except (PyJWKClientConnectionError, PyJWKSetError) as error:
            raise KeysUnavailable("could not obtain the signing keys") from error
        except PyJWKClientError as error:
            raise UnknownSigningKey(str(error)) from error
        except jwt.PyJWTError as error:
            raise InvalidToken("malformed token") from error
