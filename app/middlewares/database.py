from typing import Any, NoReturn

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models import *
from app.services.db_ctx import DatabaseContext


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, session_pool: sessionmaker):
        self.session_pool = session_pool
        super().__init__()

    async def pre_process(self, obj: TelegramObject, data: dict, *args: Any) -> NoReturn:
        session: AsyncSession = self.session_pool()
        data['user_db'] = DatabaseContext(session, query_model=User)
        data['session'] = session

    async def post_process(self, obj: TelegramObject, data: dict, *args: Any) -> NoReturn:
        if session := data.get('session', None):
            session: AsyncSession
            await session.close()
