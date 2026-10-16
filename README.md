# LES-C

## Running the auth demo locally

Prerequisites: Docker, [uv](https://docs.astral.sh/uv/), Node 20+.

1. **Database:** `cd patas-backend && docker compose up -d db` (Postgres on host port 5433)
2. **Backend:** `uv sync && uv run alembic upgrade head`, then
   `uv run uvicorn patas_backend.main:create_app --factory --port 8000`
3. **Frontend:** `cd patas-frontend`, copy `.env.example` to `.env.local` and set
   `BETTER_AUTH_SECRET` to a long random string, then
   `npm install && npx auth@latest migrate -y && npm run dev`
4. **Try it:** open http://localhost:3000/register, create an account, then log in at /login.
5. **Check the handoff end to end:** `npm run smoke:auth` (in `patas-frontend`) registers a
   user, gets a JWT and calls FastAPI `GET /me`. It should print `OK`.
6. **Tests:** `cd patas-backend && uv run pytest` and `uv run ruff check .`

Windows note: if your environment sets `SSLKEYLOGFILE` (some antivirus products do),
Python crashes with `OPENSSL_Applink`. Unset it first (PowerShell: `$env:SSLKEYLOGFILE=$null`).
