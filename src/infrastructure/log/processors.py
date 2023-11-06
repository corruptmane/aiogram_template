import sys
from collections.abc import Callable
from typing import Any
from uuid import UUID

import orjson
import structlog

from .config import LoggingConfig
from .exception_formatter import exception_formatter_factory

ProcessorType = Callable[
    [structlog.types.WrappedLogger, str, structlog.types.EventDict],
    str | bytes
]


def additionally_serialize(obj: Any) -> Any:
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError(f"TypeError: Type is not JSON serializable: {type(obj)}")


# noinspection PyUnusedLocal
def serialize_to_json(data: Any, default: Any) -> str:
    return orjson.dumps(data, default=additionally_serialize).decode()


def get_render_processor(
        config: LoggingConfig,
        serializer: Callable[..., str | bytes] = serialize_to_json,
) -> ProcessorType:
    if not sys.stderr.isatty() or config.render_json_logs:
        return structlog.processors.JSONRenderer(serializer=serializer)
    return structlog.dev.ConsoleRenderer(colors=True, exception_formatter=exception_formatter_factory(config))


def dict_tracebacks(config: LoggingConfig) -> structlog.processors.ExceptionRenderer:
    kwargs = {'show_locals': config.show_locals}
    if config.locals_max_string is not None:
        kwargs['locals_max_string'] = config.locals_max_string
    if config.max_frames is not None:
        kwargs['max_frames'] = config.max_frames
    return structlog.processors.ExceptionRenderer(structlog.tracebacks.ExceptionDictTransformer(**kwargs))
