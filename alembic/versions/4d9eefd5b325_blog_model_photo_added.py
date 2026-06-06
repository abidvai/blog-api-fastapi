"""blog model photo added

Revision ID: 4d9eefd5b325
Revises: fc8b6cf03a1c
Create Date: 2026-06-06 23:24:16.907239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4d9eefd5b325'
down_revision: Union[str, Sequence[str], None] = 'fc8b6cf03a1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('blogs', sa.Column('photo_url', sa.String(255), nullable=True))

def downgrade() -> None:
    op.drop_column('blogs', 'photo_url')