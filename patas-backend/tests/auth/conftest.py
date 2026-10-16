import json
import threading
from collections.abc import AsyncIterator, Callable, Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import httpx
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine
from token_issuer import AUDIENCE, ISSUER, TokenIssuer

from patas_backend.auth.keys import JwksKeyProvider, StaticJwksKeyProvider
from patas_backend.config import Settings
from patas_backend.main import create_app

ClientFactory = Callable[[JwksKeyProvider], httpx.AsyncClient]


@pytest_asyncio.fixture
async def make_client(
    engine: AsyncEngine, migrated_database_url: str
) -> AsyncIterator[ClientFactory]:
    """Builds clients for the real FastAPI app, wired to the test database."""
    settings = Settings(
        database_url=migrated_database_url, jwt_issuer=ISSUER, jwt_audience=AUDIENCE
    )
    clients: list[httpx.AsyncClient] = []
    apps = []

    def build(key_provider: JwksKeyProvider) -> httpx.AsyncClient:
        app = create_app(settings, key_provider)
        client = httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://testserver"
        )
        apps.append(app)
        clients.append(client)
        return client

    yield build
    for client in clients:
        await client.aclose()
    for app in apps:
        await app.state.engine.dispose()


@pytest.fixture
def client(make_client: ClientFactory, issuer: TokenIssuer) -> httpx.AsyncClient:
    return make_client(StaticJwksKeyProvider(issuer.jwks()))


@pytest.fixture
def issuer() -> TokenIssuer:
    return TokenIssuer()


@pytest.fixture
def other_issuer() -> TokenIssuer:
    """A different keypair that reuses the same key id."""
    return TokenIssuer()


@pytest.fixture
def jwks_url(issuer: TokenIssuer) -> Iterator[str]:
    """A real local HTTP server publishing the issuer's JWKS."""
    body = json.dumps(issuer.jwks()).encode()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: Any) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}/jwks"
    server.shutdown()
    server.server_close()
