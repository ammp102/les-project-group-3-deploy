# LES-C

## Run the application with Docker Compose

Docker Compose runs PostgreSQL, the FastAPI backend, and the Next.js frontend. You do
not need to install Python, `uv`, Node.js, or pnpm on your machine.

### Prerequisites

- Docker Engine with the Docker Compose v2 plugin
- Ports `3000`, `5433`, and `8000` available on your machine

Run all commands below from the repository root, where `docker-compose.yml` is located.

### Configure the development environment (optional)

Compose has development defaults for the database credentials and authentication
secrets, so the application can be started without a local environment file. These
defaults are for local development only and must not be used in a deployed environment.

To override them, create a `.env` file in the repository root. For example:

```dotenv
POSTGRES_USER=patas_admin
POSTGRES_PASSWORD=choose-a-local-password
POSTGRES_DB=patas_db
JWT_SECRET=replace-with-a-long-random-secret
BETTER_AUTH_SECRET=replace-with-a-different-long-random-secret
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
ALLOWED_ORIGINS=http://localhost:3000
```

Keep the database password consistent with any other service configuration you add.
Compose reads this file automatically. The root `.env` is ignored by Git; never commit
production secrets.

### First-time setup

1. Start PostgreSQL and wait for its health check:

   ```sh
   docker compose up -d db
   docker compose ps
   ```

   PostgreSQL is available to tools on your machine at `localhost:5433`. Containers
   connect to it using the Compose service name `db`. Alembic owns the application
   schema and creates it in the next step; `database/create.sql` is retained as a
   reference and is not run by Compose.

2. Apply the backend's Alembic migrations. These create/update the domain tables and
   the `patas_auth` schema used by Better Auth:

   ```sh
   docker compose run --build --rm backend alembic upgrade head
   ```

3. Create or update Better Auth's tables in `patas_auth`:

   ```sh
   docker compose run --build --rm frontend-migrate
   ```

   This one-off service is built from the frontend's migrator Docker target. It uses
   `pnpm dlx` to download and run the `auth` CLI, so the container needs internet access
   when the migration runs. The migrator uses Node 22 for CLI compatibility; this does
   not change the Node version used by the frontend. It is separate from the web
   frontend, so it does not run every time the app starts.

4. Build and start the backend and frontend:

   ```sh
   docker compose up --build -d backend frontend
   docker compose ps
   ```

   Open <http://localhost:3000/register> to create an account, then sign in at
   <http://localhost:3000/login>. The frontend is on port `3000`, the backend API is
   on port `8000`, and PostgreSQL is published on port `5433`.

### Applying migrations after updates

When a backend or frontend change adds a database migration, run the corresponding
command from the repository root before restarting the application:

```sh
docker compose run --build --rm backend alembic upgrade head
docker compose run --build --rm frontend-migrate
docker compose up --build -d backend frontend
```

The backend migration command is safe to run when there are no new migrations. Run
the frontend migration command when Better Auth's schema or dependencies have changed.

### Running tests and checks

The backend test suite uses PostgreSQL. Start the Compose database from the repository
root, then install the backend's development dependencies and run the tests:

```sh
docker compose up -d db
cd patas-backend
uv sync --group dev
uv run pytest
```

The tests create and reset a separate `patas_test` database, so the configured database
user must be allowed to create databases. To run the backend linter as well:

```sh
uv run ruff check .
```

### Logs and stopping the application

```sh
docker compose logs -f backend frontend db
docker compose down
```

`docker compose down` preserves the PostgreSQL data volume. To intentionally delete
the local database and all its data as well, use `docker compose down -v`.
