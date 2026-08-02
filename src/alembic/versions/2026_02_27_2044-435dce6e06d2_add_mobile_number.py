"""add mobile number

Revision ID: 435dce6e06d2
Revises: 6ee103598b72
Create Date: 2026-02-27 20:44:55.347592

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "435dce6e06d2"
down_revision: Union[str, Sequence[str], None] = "6ee103598b72"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("profiles", sa.Column("mobile", sa.String(), nullable=True))
    op.alter_column(
        "profiles", "first_name", existing_type=sa.VARCHAR(), nullable=False
    )


def downgrade() -> None:
    op.alter_column("profiles", "first_name", existing_type=sa.VARCHAR(), nullable=True)
    op.drop_column("profiles", "mobile")
