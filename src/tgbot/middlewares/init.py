from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infrastructure.db.dao.holder import HolderDAO
from src.tgbot.config import Config
from src.tgbot.utils.data import MiddlewareData


class InitMiddleware(BaseMiddleware):
    def __init__(
            self, *,
            session_factory: async_sessionmaker[AsyncSession],
            config: Config,
            redis: Redis,
    ) -> None:
        self.session_factory = session_factory
        self.config = config
        self.redis = redis

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData,
    ) -> Any:
        data['config'] = self.config
        async with self.session_factory() as session:
            data['dao'] = HolderDAO(session)
            result = await handler(event, data)
            del data['dao']
        return result
