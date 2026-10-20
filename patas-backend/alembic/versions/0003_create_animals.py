"""create animals

Revision ID: 0003
Revises: 0002
"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    species_type = postgresql.ENUM(
        "CAT",
        "DOG",
        "RABBIT",
        name="species",
        schema="patas",
        create_type=False,
    )
    species_type.create(op.get_bind(), checkfirst=True)
    if not sa.inspect(op.get_bind()).has_table("animal", schema="patas"):
        op.create_table(
            "animal",
            sa.Column("id", sa.UUID(), primary_key=True),
            sa.Column("species", species_type, nullable=False),
            sa.Column("name", sa.Text(), nullable=False),
            sa.Column("owner_id", sa.UUID(), nullable=False),
            sa.CheckConstraint(
                "char_length(btrim(name)) > 0", name="animal_name_not_blank_check"
            ),
            schema="patas",
        )
    op.execute(
        """
        INSERT INTO patas.animal (id, species, name, owner_id)
        VALUES
            (
                '10000000-0000-4000-8000-000000000001',
                'CAT',
                'Milo',
                '20000000-0000-4000-8000-000000000001'
            ),
            (
                '10000000-0000-4000-8000-000000000002',
                'DOG',
                'Luna',
                '20000000-0000-4000-8000-000000000001'
            ),
            (
                '10000000-0000-4000-8000-000000000003',
                'RABBIT',
                'Pipoca',
                '20000000-0000-4000-8000-000000000002'
            ),
            (
                '10000000-0000-4000-8000-000000000004',
                'CAT',
                'Nina',
                '20000000-0000-4000-8000-000000000002'
            ),
            (
                '10000000-0000-4000-8000-000000000005',
                'DOG',
                'Bobby',
                '20000000-0000-4000-8000-000000000003'
            ),
            (
                '10000000-0000-4000-8000-000000000006',
                'RABBIT',
                'Cenoura',
                '20000000-0000-4000-8000-000000000003'
            )
        ON CONFLICT (id) DO NOTHING
        """
    )


def downgrade() -> None:
    op.drop_table("animal", schema="patas")
    op.execute("DROP TYPE patas.species")
