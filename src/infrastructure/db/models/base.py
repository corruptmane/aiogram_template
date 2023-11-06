from typing import Any

from sqlalchemy import inspect, MetaData
from sqlalchemy.orm import DeclarativeMeta, registry

convention = {
    "ix": "ix__%(column_0_label)s",
    "uq": "uq__%(table_name)s__%(column_0_name)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "pk__%(table_name)s",
}
metadata = MetaData(naming_convention=convention)
mapper_registry = registry(metadata=metadata)


class BaseModel(metaclass=DeclarativeMeta):
    __abstract__ = True
    __mapper_args__ = {'eager_defaults': True}

    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    registry = mapper_registry
    metadata = mapper_registry.metadata

    def _get_attributes(self) -> dict[Any, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def __str__(self) -> str:
        attrs = '|'.join(str(v) for k, v in self._get_attributes().items())
        return f'{self.__class__.__qualname__} {attrs}'

    def __repr__(self) -> str:
        table_attrs = inspect(self).attrs
        primary_keys = ' '.join(
            f'{key.name}={table_attrs[key.name].value}'
            for key in inspect(self.__class__).primary_key
        )
        return f'{self.__class__.__qualname__}->{primary_keys}'

    def as_dict(self) -> dict[Any, Any]:
        return self._get_attributes()
