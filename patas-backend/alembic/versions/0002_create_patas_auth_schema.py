"""create patas_auth schema

Better-Auth (Next.js) owns the tables inside this schema; Alembic only creates it,
so the order is `alembic upgrade head` and then `npx auth@latest migrate`.

Revision ID: 0002
Revises: 0001
"""

from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS patas_auth")


def downgrade() -> None:
    # No CASCADE on purpose: this refuses to drop a schema that holds accounts.
    op.execute("DROP SCHEMA IF EXISTS patas_auth")
