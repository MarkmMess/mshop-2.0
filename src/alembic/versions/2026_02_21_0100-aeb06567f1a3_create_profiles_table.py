"""create profiles table

Revision ID: aeb06567f1a3
Revises: 797816634390
Create Date: 2026-02-21 01:00:23.633472

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "aeb06567f1a3"
down_revision: Union[str, Sequence[str], None] = "797816634390"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("bio", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("profiles")
