from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import ContentType, Message


async def start_bot(msg: Message) -> NoReturn:
    await msg.answer(f"Hello, {msg.from_user.full_name}!")


def setup(dispatcher: Dispatcher) -> NoReturn:
    dispatcher.register_message_handler(
        start_bot, Command("start"), content_types=ContentType.TEXT, state="*"
    )


__all__ = ["setup"]
