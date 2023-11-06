from typing import Any, Callable, Awaitable

import structlog
from aiogram import BaseMiddleware
from aiogram.types import Update

from src.tgbot.utils.data import AiogramMiddlewareData


class ContextMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: AiogramMiddlewareData,
    ) -> Any:
        user = data['event_from_user']
        with structlog.contextvars.bound_contextvars(user_id=user.id, update_id=event.update_id):
            return await handler(event, data)
