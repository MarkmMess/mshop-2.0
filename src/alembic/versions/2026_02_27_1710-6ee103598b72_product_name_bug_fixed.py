"""product name bug fixed

Revision ID: 6ee103598b72
Revises: aeb06567f1a3
Create Date: 2026-02-27 17:10:59.672502

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6ee103598b72"
down_revision: Union[str, Sequence[str], None] = "aeb06567f1a3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("name", sa.String(length=100), nullable=False))


def downgrade() -> None:
    op.drop_column("products", "name")
