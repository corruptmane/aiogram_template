import structlog
from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import User
from aiogram.types.error_event import ErrorEvent
from aiogram_dialog.api.exceptions import UnknownIntent

from src.tgbot.views.error import answer_user, go_to_start

log = structlog.get_logger(__name__)

router = Router(name='routers.error')


@router.errors(ExceptionTypeFilter(UnknownIntent))
async def handle_unknown_intent_error(err_event: ErrorEvent) -> None:
    await log.aerror('Restarting dialog: %s', err_event.exception)
    text = 'Bot was restarted due to maintenance.\n\nRedirecting to main menu.'
    await answer_user(err_event, text)
    await go_to_start(err_event)


@router.errors(ExceptionTypeFilter(TelegramBadRequest))
async def bad_request_error(_, bot: Bot, event_from_user: User) -> None:
    await bot.send_message(chat_id=event_from_user.id, text='Unfortunately, but something went wrong. Try again')


@router.errors()
async def handle_all_other_errors(error_event: ErrorEvent) -> None:
    await log.aexception('Unhandled error: %s', error_event.exception, exc_info=error_event.exception)
    await answer_user(error_event, 'Sorry, but something went wrong...')
