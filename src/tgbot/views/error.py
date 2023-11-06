from typing import cast

from aiogram.types import ErrorEvent, Message
from aiogram.utils.callback_answer import CallbackAnswer

from src.tgbot.handlers.start import msg_start_handler


async def go_to_start(event: ErrorEvent) -> None:
    match event.update.event_type:
        case 'message':
            await msg_start_handler(cast(Message, event.update.event))
        case _:
            raise NotImplementedError


async def answer_user(err_event: ErrorEvent, text: str, callback_answer: CallbackAnswer | None = None) -> None:
    match err_event.update.event_type:
        case 'message':
            await err_event.update.message.answer(text)
        case 'callback_query':
            if callback_answer is None:
                await err_event.update.callback_query.answer(text, show_alert=True)
                return
            callback_answer.text = text
            callback_answer.show_alert = True
        case _:
            raise NotImplementedError
