"""create users

Revision ID: 0001
Revises:
"""

import sqlalchemy as sa

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS patas")
    op.execute(
        """
        CREATE FUNCTION patas.set_updated_at() RETURNS trigger AS $$
        BEGIN
            NEW.updated_at := now();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
        """
    )
    op.create_table(
        "users",
        # No default: the id always comes from the Better-Auth JWT `sub`.
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.Column(
            "is_platform_admin",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.CheckConstraint(
            "char_length(btrim(name)) > 0", name="users_name_not_blank_check"
        ),
        sa.CheckConstraint(
            "char_length(btrim(email)) > 0", name="users_email_not_blank_check"
        ),
        sa.CheckConstraint(
            "position('@' in email) > 1", name="users_email_format_check"
        ),
        schema="patas",
    )
    op.execute(
        "CREATE UNIQUE INDEX idx_users_email_lower ON patas.users (lower(email))"
    )
    op.execute(
        """
        CREATE TRIGGER trigger_users_set_updated_at
        BEFORE UPDATE ON patas.users
        FOR EACH ROW EXECUTE FUNCTION patas.set_updated_at()
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER trigger_users_set_updated_at ON patas.users")
    op.execute("DROP INDEX patas.idx_users_email_lower")
    op.drop_table("users", schema="patas")
    op.execute("DROP FUNCTION patas.set_updated_at()")
