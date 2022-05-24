import logging

from aiogram import Dispatcher
from aiogram.types import Update
from aiogram.utils.exceptions import (
    BadRequest, CantDemoteChatCreator, CantParseEntities, InvalidQueryID,
    MessageCantBeDeleted, MessageNotModified, MessageTextIsEmpty,
    MessageToDeleteNotFound, RetryAfter, TelegramAPIError, Unauthorized
)

log = logging.getLogger(__name__)


async def errors_handler(update: Update, exception):
    if isinstance(exception, CantDemoteChatCreator):
        log.debug("Can't demote chat creator")
        return True
    if isinstance(exception, MessageNotModified):
        log.debug('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        log.info('Message cant be deleted')
        return True
    if isinstance(exception, MessageToDeleteNotFound):
        log.info('Message to delete not found')
        return True
    if isinstance(exception, MessageTextIsEmpty):
        log.debug('MessageTextIsEmpty')
        return True
    if isinstance(exception, Unauthorized):
        log.info(f'Unauthorized: {exception}')
        return True
    if isinstance(exception, InvalidQueryID):
        log.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, CantParseEntities):
        log.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        log.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, BadRequest):
        log.exception(f'BadRequest: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, TelegramAPIError):
        log.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    log.exception(f'Update: {update} \n{exception}')


def setup(dp: Dispatcher) -> None:
    dp.register_errors_handler(errors_handler)
