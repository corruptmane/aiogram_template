"""init

Revision ID: d2245d4be86e
Revises: 
Create Date: 2022-08-26 20:35:55.599657

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd2245d4be86e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=False),
        sa.Column('full_name', sa.VARCHAR(length=255), nullable=False),
        sa.Column('mention', sa.VARCHAR(length=300), nullable=False),
        sa.Column('active', sa.BOOLEAN(), server_default=sa.text('true'), nullable=False),
        sa.Column('referrer_id', sa.BIGINT(), nullable=True),
        sa.ForeignKeyConstraint(['referrer_id'], ['users.user_id'], name='FK__users_referrer_id', ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_users_referrer_id'), 'users', ['referrer_id'], unique=False)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_index(op.f('ix_users_referrer_id'), table_name='users')
    op.drop_table('users')
