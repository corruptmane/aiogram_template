import logging

from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker

from tgbot.middlewares.acl import ACLMiddleware
from tgbot.middlewares.chat_type import RestrictChatTypesMiddleware
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.middlewares.throttling import ThrottlingMiddleware

log = logging.getLogger(__name__)


def setup(dp: Dispatcher, allowed_chat_types: list, session_pool: sessionmaker, rate_limit: float):
    dp.setup_middleware(RestrictChatTypesMiddleware(allowed_chat_types=allowed_chat_types))
    dp.setup_middleware(DatabaseMiddleware(session_pool))
    dp.setup_middleware(ThrottlingMiddleware(rate_limit))
    dp.setup_middleware(ACLMiddleware())
    log.info('Middlewares are successfully configured')
