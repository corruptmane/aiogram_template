import logging
from typing import NoReturn

from aiogram import Dispatcher

from app.handlers import errors, private


def setup(dispatcher: Dispatcher) -> NoReturn:
    errors.setup(dispatcher)
    private.setup(dispatcher)
    logging.info("Handlers are successfully configured")
