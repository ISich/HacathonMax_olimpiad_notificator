"""add olympiad external id

Revision ID: 76284bc22fc4
Revises: d09d31344980
Create Date: 2026-09-26 02:22:23.307833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76284bc22fc4'
down_revision: Union[str, Sequence[str], None] = 'd09d31344980'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "olympiads",
        sa.Column(
            "external_id",
            sa.String(length=255),
            nullable=False
        )
    )

    op.create_unique_constraint(
        "uq_olympiads_external_id",
        "olympiads",
        ["external_id"]
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_olympiads_external_id",
        "olympiads",
        type_="unique"
    )

    op.drop_column(
        "olympiads",
        "external_id"
    )
