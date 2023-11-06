import logging.config
import sys

import structlog
from sqlalchemy import log as sa_log

from .config import LoggingConfig
from .processors import get_render_processor, dict_tracebacks


def _mute_loggers() -> None:
    # Mute SQLAlchemy default logger handler
    sa_log._add_default_handler = lambda _: None
    # Mute Uvicorn loggers
    logging.getLogger('uvicorn.error').disabled = True
    logging.getLogger('uvicorn.access').disabled = True
    # Mute taskiq process-manager logger
    logging.getLogger('taskiq.process-manager').disabled = True


def configure_logging(config: LoggingConfig) -> None:
    _mute_loggers()

    common_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.ExtraAdder(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S.%f", utc=True),
        structlog.contextvars.merge_contextvars,
        structlog.processors.CallsiteParameterAdder((
            structlog.processors.CallsiteParameter.FUNC_NAME,
            structlog.processors.CallsiteParameter.LINENO,
            structlog.processors.CallsiteParameter.MODULE,
        )),
    ]
    if not sys.stderr.isatty() or config.render_json_logs:
        common_processors.append(dict_tracebacks(config))
    common_processors = tuple(common_processors)

    structlog_processors = (
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    )

    logging_processors = (
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        get_render_processor(config),
    )

    handler = logging.StreamHandler()
    handler.set_name("default")
    handler.setLevel(config.level)
    console_formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=common_processors,
        processors=logging_processors,
    )
    handler.setFormatter(console_formatter)

    logging.basicConfig(handlers=[handler], level=config.level)
    # noinspection PyTypeChecker
    structlog.configure(
        processors=common_processors + structlog_processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
