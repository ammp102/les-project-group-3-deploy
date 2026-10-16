import jwt

from patas_backend.auth.authenticated_principal import (
    AuthenticatedPrincipal,
    InvalidClaims,
)
from patas_backend.auth.errors import InvalidToken
from patas_backend.auth.keys import JwksKeyProvider

# The algorithm is decided here, never taken from the (attacker-controlled) token
# header. This is what defeats `alg: none` and HS256-with-the-public-key tricks.
ALLOWED_ALGORITHMS = ["EdDSA"]
REQUIRED_CLAIMS = ["exp", "iss", "aud", "sub"]


class JwtVerifier:
    def __init__(self, keys: JwksKeyProvider, *, issuer: str, audience: str) -> None:
        self._keys = keys
        self._issuer = issuer
        self._audience = audience

    def verify(self, token: str) -> AuthenticatedPrincipal:
        key = self._keys.signing_key_for(token)
        try:
            claims = jwt.decode(
                token,
                key.key,
                algorithms=ALLOWED_ALGORITHMS,
                issuer=self._issuer,
                audience=self._audience,
                options={"require": REQUIRED_CLAIMS},
            )
            return AuthenticatedPrincipal.from_claims(claims)
        except (jwt.PyJWTError, InvalidClaims) as error:
            raise InvalidToken(str(error)) from error
