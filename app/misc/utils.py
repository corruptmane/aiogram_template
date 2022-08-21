import logging
from contextlib import suppress
from typing import TypeVar

from aiogram.types import Message

log = logging.getLogger(__name__)


async def clear_last_message(data: dict, msg: Message):
    msg_id = int(data.get('last_msg_id'))
    with suppress(Exception):
        await msg.bot.delete_message(msg.from_user.id, msg_id)


Element = TypeVar('Element')


def generate_pages(array: list[Element], elements_on_page: int) -> list[list[Element]]:
    elements_quantity = len(array)
    pages_quantity = (elements_quantity // elements_on_page)
    if elements_quantity % elements_on_page != 0:
        pages_quantity += 1
    results = [array[page * elements_on_page: (page + 1) * elements_on_page] for page in range(pages_quantity)]
    return results


def set_rate_limit(limit: int, key: str | None = None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


def set_clocks():
    def decorator(func):
        setattr(func, 'clocks', True)
        return func

    return decorator


def set_answered():
    def decorator(func):
        setattr(func, 'is_answered', True)
        return func

    return decorator


__all__ = (
    'clear_last_message',
    'generate_pages',
    'set_rate_limit',
    'set_clocks',
    'set_answered',
)
