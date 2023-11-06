"""init

Revision ID: 53486a2f348d
Revises: 
Create Date: 2023-11-06 20:39:46.996354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '53486a2f348d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column('full_name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('username', sa.VARCHAR(length=33), nullable=True),
        sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('user_id', name=op.f('pk__users'))
    )


def downgrade() -> None:
    op.drop_table('users')
