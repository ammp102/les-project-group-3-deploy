class InvalidToken(Exception):
    """The bearer token must not be trusted (maps to HTTP 401)."""


class UnknownSigningKey(InvalidToken):
    """The token names a key id that is not in the JWKS."""


class KeysUnavailable(Exception):
    """The signing keys cannot be obtained right now (maps to HTTP 503)."""
