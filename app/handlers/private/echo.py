from typing import NoReturn

from aiogram import Dispatcher
from aiogram.types import ContentTypes, Message


async def echo_bot(msg: Message) -> NoReturn:
    await msg.answer(f"Echo mode. Your message:\n\n{msg.text}")


def setup(dispatcher: Dispatcher) -> NoReturn:
    dispatcher.register_message_handler(
        echo_bot, state="*", content_types=ContentTypes.TEXT
    )


__all__ = ["setup"]
