from contextlib import suppress
from typing import Any

from aiogram.types import Message
from aiogram.utils.exceptions import MessageError


async def clear_last_message(data: dict, msg: Message):
    msg_id = int(data.get('msg_id'))
    with suppress(MessageError):
        await msg.bot.delete_message(msg.from_user.id, msg_id)


def generate_pages(array: list[Any], elements_on_page: int) -> list[list[Any]]:
    length = len(array)
    pages_quantity = (length // elements_on_page)
    if elements_on_page == 0:
        pages_quantity += 1
    return [array[page * elements_on_page : (page + 1) * elements_on_page] for page in range(pages_quantity)]


def rate_limit(limit: int, key: str | None = None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


def answered_cb():
    def decorator(func):
        setattr(func, 'answered_cb', True)
        return func

    return decorator


answered = answered_cb()
