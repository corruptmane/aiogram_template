import asyncio
from typing import Union

from aiogram import Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit: float = DEFAULT_RATE_LIMIT, key_prefix: str = 'antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def throttle(self, target: Union[Message, CallbackQuery]):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if not handler:
            return
        limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
        key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.target_throttled(target, t, dispatcher, key)
            raise CancelHandler()

    @staticmethod
    async def target_throttled(target: Union[Message, CallbackQuery],
                               throttled: Throttled, dispatcher: Dispatcher, key: str):
        msg = target.message if isinstance(target, CallbackQuery) else target
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count == 2:
            await msg.reply('Слишком Часто! Давай не так быстро')
            return
        elif throttled.exceeded_count == 3:
            await msg.reply(f'Всё. Больше не отвечу, пока не пройдет {delta} секунд')
            return
        await asyncio.sleep(delta)

        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await msg.reply("Все, теперь отвечаю.")

    async def on_process_message(self, message: Message, data: dict):
        await self.throttle(message)

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        await self.throttle(call)
