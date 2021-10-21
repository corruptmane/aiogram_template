import sqlalchemy as sa

from app.models.base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"

    user_id = sa.Column(sa.BigInteger, primary_key=True, index=True)
    full_name = sa.Column(sa.String, nullable=False)
    mention = sa.Column(sa.String, nullable=False)
    mailing = sa.Column(
        sa.Boolean, server_default=sa.sql.expression.false(), index=True
    )

    is_admin = sa.Column(
        sa.Boolean, server_default=sa.sql.expression.false(), index=True
    )
    is_banned = sa.Column(
        sa.Boolean, server_default=sa.sql.expression.false(), index=True
    )

    query: sa.sql.Select
