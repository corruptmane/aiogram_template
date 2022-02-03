from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import User
from aiogram.types.base import TelegramObject

from app.config import Config


class IsAdmin(BoundFilter):
    async def check(self, obj: TelegramObject, *args) -> bool:
        config: Config = obj.bot.get('config')
        user = User.get_current()
        return user.id in config.bot.admin_ids
