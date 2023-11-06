from aiogram import Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.tgbot.config import Config
from .context import ContextMiddleware
from .init import InitMiddleware
from .load_data import LoadDataMiddleware


def setup_middlewares(
        dp: Dispatcher,
        *,
        session_factory: async_sessionmaker[AsyncSession],
        config: Config,
        redis: Redis,
) -> None:
    dp.update.outer_middleware(ContextMiddleware())
    dp.update.middleware(
        InitMiddleware(
            session_factory=session_factory,
            config=config,
            redis=redis,
        )
    )
    dp.update.middleware(LoadDataMiddleware())
    dp.callback_query.middleware(CallbackAnswerMiddleware(show_alert=True))
