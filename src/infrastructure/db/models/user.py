import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import dto
from src.infrastructure.db.models import BaseModel
from src.infrastructure.db.utils.mixin import TableNameMixin, CreatedAtMixin


class User(BaseModel, TableNameMixin, CreatedAtMixin):
    user_id: Mapped[int] = mapped_column(sa.BIGINT, primary_key=True, autoincrement=False)
    full_name: Mapped[str] = mapped_column(sa.VARCHAR(255))
    username: Mapped[str | None] = mapped_column(sa.VARCHAR(33))

    # Did user ban bot or not
    is_active: Mapped[bool] = sa.Column(sa.BOOLEAN, default=True, server_default=sa.true())

    def to_dto(self) -> dto.User:
        return dto.User(
            user_id=self.user_id,
            full_name=self.full_name,
            username=self.username,
            is_active=self.is_active,
        )
