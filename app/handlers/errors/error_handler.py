import logging
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.utils.exceptions import (BadRequest, CantDemoteChatCreator,
                                      CantParseEntities, InvalidQueryID,
                                      MessageCantBeDeleted, MessageNotModified,
                                      MessageTextIsEmpty,
                                      MessageToDeleteNotFound, RetryAfter,
                                      TelegramAPIError, Unauthorized)


async def errors_handler(update, exception) -> NoReturn:
    if isinstance(exception, Unauthorized):
        logging.info(f"Unauthorized: {exception}")
    elif isinstance(exception, InvalidQueryID):
        logging.exception(f"InvalidQueryID: {exception}\nUpdate: {update}")
    elif isinstance(exception, TelegramAPIError):
        logging.exception(f"TelegramAPIError: {exception}\nUpdate: {update}")
    elif isinstance(exception, CantDemoteChatCreator):
        logging.debug(f"Can't demote chat creator")
    elif isinstance(exception, MessageNotModified):
        logging.debug("Message is not modified")
    elif isinstance(exception, MessageToDeleteNotFound):
        logging.debug("Message to delete not found")
    elif isinstance(exception, MessageTextIsEmpty):
        logging.debug("MessageTextIsEmpty")
    elif isinstance(exception, RetryAfter):
        logging.exception(f"RetryAfter: {exception} \nUpdate: {update}")
    elif isinstance(exception, CantParseEntities):
        logging.exception(f"CantParseEntities: {exception} \nUpdate: {update}")
    elif isinstance(exception, MessageCantBeDeleted):
        logging.debug("Message cant be deleted")
    elif isinstance(exception, BadRequest):
        logging.exception(f"CantParseEntities: {exception} \nUpdate: {update}")
    else:
        logging.exception(f"Update: {update}\n{exception}")
    return True


def setup(dispatcher: Dispatcher) -> NoReturn:
    dispatcher.register_errors_handler(errors_handler)


__all__ = ["setup"]
