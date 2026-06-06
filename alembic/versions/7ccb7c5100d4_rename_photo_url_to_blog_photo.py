"""rename photo_url to blog_photo

Revision ID: 7ccb7c5100d4
Revises: 4d9eefd5b325
Create Date: 2026-06-07 00:49:08.569360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ccb7c5100d4'
down_revision: Union[str, Sequence[str], None] = '4d9eefd5b325'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('blogs', 'photo_url', new_column_name='blog_photo')

def downgrade() -> None:
    op.alter_column('blogs', 'blog_photo', new_column_name='photo_url')
