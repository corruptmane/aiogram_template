from typing import Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.core.models import dto
from src.core.services.user import upsert_user
from src.infrastructure.db.dao.holder import HolderDAO
from src.tgbot.utils.data import MiddlewareData


class LoadDataMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: MiddlewareData,
    ) -> Any:
        holder_dao = data['dao']
        tg_user = await save_tg_user(data, holder_dao)
        data['user'] = tg_user
        return await handler(event, data)


async def save_tg_user(data: MiddlewareData, holder_dao: HolderDAO) -> dto.User | None:
    user = data['event_from_user']
    if not user:
        return None
    is_admin = user.id in data['config'].bot.admin_ids
    return await upsert_user(dto.User.from_aiogram(user, is_admin), holder_dao.user)
