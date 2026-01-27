"""test empty migration

Revision ID: cb9b7c13fb88
Revises: 36f4594032ab
Create Date: 2026-01-27 22:14:58.228308

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb9b7c13fb88'
down_revision = '36f4594032ab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
