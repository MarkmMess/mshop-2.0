"""delete id column

Revision ID: a0a4a42fe43a
Revises: 435dce6e06d2
Create Date: 2026-03-01 12:05:56.552551

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a0a4a42fe43a"
down_revision: Union[str, Sequence[str], None] = "435dce6e06d2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("profiles", "id")


def downgrade() -> None:
    op.add_column(
        "profiles",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
    )
