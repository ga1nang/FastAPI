"""Create phone number for user column

Revision ID: f29c11d86d72
Revises: 
Create Date: 2024-11-26 09:25:09.896675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f29c11d86d72'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
