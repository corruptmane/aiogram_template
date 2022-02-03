import asyncio
import logging
from typing import AsyncGenerator, Any, Callable, Awaitable, Iterable

from aiogram.utils.exceptions import RetryAfter, BotBlocked, UserDeactivated, ChatNotFound, Unauthorized, \
    TelegramAPIError

from app.models import User
from app.services import DatabaseContext

log = logging.getLogger(__name__)


async def broadcast(
    chats: AsyncGenerator[int] | Any,
    action: Callable[[int, Any, ...], Awaitable[Any, int]],
    user_db: DatabaseContext[User],
    **func_kwargs: Any
) -> int:
    counter = 0
    async for chat_id in chats:
        await safely_send_message(chat_id, action, counter, user_db, **func_kwargs)
        counter += 1
    return counter


async def safely_send_message(
    chat_id: int,
    action: Callable[[int, Any, ...], Awaitable[Any, int]],
    counter: int,
    user_db: DatabaseContext[User],
    **func_kwargs: Any
):
    try:
        await action(chat_id, counter, **func_kwargs)
    except RetryAfter as e:
        log.error(f'Target [ID:{chat_id}]: Flood limit is exceeded. Sleep for {e.timeout} seconds.')
        await asyncio.sleep(e.timeout)
        await safely_send_message(chat_id, action, counter, user_db, **func_kwargs)
    except (BotBlocked, UserDeactivated, ChatNotFound, Unauthorized):
        await user_db.update(User.user_id == chat_id, active=False)
        log.error(f'Target [ID:{chat_id}]: Bad user-relationships error.')
    except TelegramAPIError:
        log.error(f'Target [ID:{chat_id}]: TelegramAPIError.')
    except Exception as e:
        log.error(f'Target [ID:{chat_id}]: {e.__class__.__name__} error')
    finally:
        await asyncio.sleep(0.05)


async def from_iterable(it: Iterable) -> AsyncGenerator:
    for item in it:
        await asyncio.sleep(0)
        yield item
