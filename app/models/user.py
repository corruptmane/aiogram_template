import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.models.base import BaseModel, TimestampMixin


class User(BaseModel, TimestampMixin):
    user_id = sa.Column(sa.BIGINT, primary_key=True, autoincrement=False, index=True)
    full_name = sa.Column(sa.VARCHAR(255), nullable=False)
    mention = sa.Column(sa.VARCHAR(300), nullable=False)

    active = sa.Column(sa.BOOLEAN, default=True, server_default=sa.true(), nullable=False)

    referrer_id = sa.Column(
        sa.BIGINT, sa.ForeignKey('users.user_id', ondelete='SET NULL', name='FK__users_referrer_id'),
        nullable=True, index=True
    )

    referrer: 'User' = relationship(
        'User',
        back_populates='referrals',
        remote_side=[user_id],
        uselist=False
    )

    referrals: list['User'] = relationship(
        'User',
        back_populates='referrer',
        remote_side=[referrer_id],
        innerjoin=True
    )
