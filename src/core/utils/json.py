from typing import Protocol, Any, Callable

import orjson


class JsonLoads(Protocol):
    def __call__(self, s: str) -> Any:
        raise NotImplementedError


class JsonDumps(Protocol):
    def __call__(self, obj: Any) -> str:
        raise NotImplementedError


def orjson_dumps(
        value: Any,
        *,
        default: Callable[[Any], Any] | None = None,
        option: int | None = None,
) -> str:
    return orjson.dumps(value, default=default, option=option).decode()


__all__ = (
    'JsonLoads',
    'JsonDumps',
    'orjson_dumps',
)
