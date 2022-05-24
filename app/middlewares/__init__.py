import logging
from typing import Any

from aiogram import Dispatcher
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from sqlalchemy.orm import sessionmaker

from app.middlewares.acl import ACLMiddleware
from app.middlewares.clocks import ClocksMiddleware
from app.middlewares.database import DatabaseMiddleware
from app.middlewares.throttling import ThrottlingMiddleware

log = logging.getLogger(__name__)


def setup(
        dp: Dispatcher, session_pool: sessionmaker, rate_limit: float, environments: dict[str: Any]
) -> None:
    dp.setup_middleware(EnvironmentMiddleware(environments))
    dp.setup_middleware(DatabaseMiddleware(session_pool))
    dp.setup_middleware(ThrottlingMiddleware(rate_limit))
    dp.setup_middleware(ClocksMiddleware())
    dp.setup_middleware(ACLMiddleware())
    log.info('Middlewares are successfully configured')
