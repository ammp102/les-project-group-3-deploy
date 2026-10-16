import asyncio
import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from patas_backend.auth.errors import InvalidToken, KeysUnavailable
from patas_backend.models.user import EmailAlreadyRegistered, User, UserRepository

logger = logging.getLogger(__name__)

# auto_error=False: a missing header or a non-Bearer scheme yields None, so every
# authentication failure goes through the same 401 below.
bearer = HTTPBearer(auto_error=False)


def _unauthorized() -> HTTPException:
    # Same generic body for every cause: callers cannot tell why a token failed.
    return HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    request: Request,
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> User:
    """Verify the Bearer JWT and return the stored user, creating it on first use."""
    if credentials is None:
        raise _unauthorized()

    try:
        # PyJWKClient does blocking I/O when it fetches keys, so keep it off the loop.
        principal = await asyncio.to_thread(
            request.app.state.verifier.verify, credentials.credentials
        )
    except InvalidToken as error:
        logger.info("rejected token: %s", error)
        raise _unauthorized() from error
    except KeysUnavailable as error:
        logger.error("signing keys unavailable: %s", error)
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Authentication service temporarily unavailable",
        ) from error

    user = User.provision(id=principal.id, name=principal.name, email=principal.email)
    try:
        # Its own short transaction: provisioning commits immediately and does not
        # depend on whatever the endpoint does afterwards.
        async with request.app.state.session_factory.begin() as session:
            return await UserRepository(session).ensure_exists(user)
    except EmailAlreadyRegistered as error:
        logger.warning("email already registered to another user: %s", user.email)
        raise _unauthorized() from error
