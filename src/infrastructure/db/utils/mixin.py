from datetime import datetime
from re import split, compile
from typing import cast, Type, Pattern, Final

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import declarative_mixin, Mapped, mapped_column, declared_attr, has_inherited_table

from src.infrastructure.db.models.base import BaseModel

TABLE_NAME_REGEX: Pattern[str] = compile(r'(?<=[A-Z])(?=[A-Z][a-z])|(?<=[^A-Z])(?=[A-Z])')
PLURAL: Final[str] = 's'


@declarative_mixin
class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())


@declarative_mixin
class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), server_default=func.now(), onupdate=func.now(),
    )


@declarative_mixin
class TableNameMixin:
    @declared_attr
    def __tablename__(self) -> str | None:
        if has_inherited_table(cast(Type[BaseModel], self)):
            return None
        cls_name = cast(Type[BaseModel], self).__qualname__
        table_name_parts = split(TABLE_NAME_REGEX, cls_name)
        formatted_table_name = ''.join(
            table_name_part.lower() + '_' for i, table_name_part in enumerate(table_name_parts)
        )
        last_underscore = formatted_table_name.rfind('_')
        return formatted_table_name[:last_underscore] + PLURAL
