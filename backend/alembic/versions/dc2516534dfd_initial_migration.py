"""Initial migration

Revision ID: dc2516534dfd
Revises: 7846d0d1dfc6
Create Date: 2025-07-27 12:17:09.416107

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dc2516534dfd"
down_revision: Union[str, Sequence[str], None] = "7846d0d1dfc6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
