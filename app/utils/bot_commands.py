from typing import NoReturn

from aiogram import Dispatcher
from aiogram.types import BotCommand


async def setup_default_commands(dispatcher: Dispatcher) -> NoReturn:
    await dispatcher.bot.set_my_commands(
        [BotCommand("start", "Запустить бота"), BotCommand("help", "Помощь")]
    )
