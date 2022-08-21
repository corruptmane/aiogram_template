import asyncio
from typing import Union, NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit: float = DEFAULT_RATE_LIMIT, key_prefix: str = 'antiflood_') -> None:
        super(ThrottlingMiddleware, self).__init__()
        self.rate_limit = limit
        self.prefix = key_prefix

    async def throttle(self, target: Union[Message, CallbackQuery]) -> NoReturn | None:
        handler = current_handler.get()
        if not handler:
            return

        dispatcher = self.manager.dispatcher
        limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
        key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")

        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.target_throttled(target, t, dispatcher, key)
            raise CancelHandler()

    @staticmethod
    async def target_throttled(
            target: Union[Message, CallbackQuery], throttled: Throttled, dispatcher: Dispatcher, key: str
    ) -> None:
        msg = target.message if isinstance(target, CallbackQuery) else target
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count == 2:
            await msg.reply('Too often! Let\'s not go so fast')
            return
        elif throttled.exceeded_count == 3:
            await msg.reply(f'Done. I won\'t answer you again until {delta} seconds have passed')
            return
        await asyncio.sleep(delta)

        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await msg.reply('That\'s it, now we can continue the conversation')

    async def on_process_message(self, message: Message, data: dict) -> None:  # NOQA
        await self.throttle(message)

    async def on_process_callback_query(self, call: CallbackQuery, data: dict) -> None:  # NOQA
        await self.throttle(call)
