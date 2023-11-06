from typing import Callable, TextIO

from structlog.dev import plain_traceback
from structlog.typing import ExcInfo

from .config import LoggingConfig


def exception_formatter_factory(config: LoggingConfig) -> Callable[[TextIO, ExcInfo], None]:
    try:
        from .rich import RichExceptionFormatter
    except ImportError:
        return plain_traceback
    return RichExceptionFormatter(config)
