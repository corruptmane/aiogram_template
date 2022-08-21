import logging
from typing import Any

from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker

from app.config import Config
from app.middlewares.acl import ACLMiddleware
from app.middlewares.clocks import ClocksMiddleware
from app.middlewares.database import DatabaseMiddleware
from app.middlewares.environment import EnvironmentMiddleware
from app.middlewares.sentry import SentryContextMiddleware
from app.middlewares.throttling import ThrottlingMiddleware

log = logging.getLogger(__name__)


def setup(
        dp: Dispatcher, session_pool: sessionmaker, rate_limit: float, environments: dict[str: Any]
) -> None:
    config: Config = environments.get('config')
    if config.misc.sentry_dsn is not None:
        dp.setup_middleware(SentryContextMiddleware())
    dp.setup_middleware(EnvironmentMiddleware(environments))
    dp.setup_middleware(DatabaseMiddleware(session_pool))
    dp.setup_middleware(ThrottlingMiddleware(rate_limit))
    dp.setup_middleware(ClocksMiddleware())
    dp.setup_middleware(ACLMiddleware())
    log.info('Middlewares are successfully configured')
