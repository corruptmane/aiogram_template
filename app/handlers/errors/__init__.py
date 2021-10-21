from typing import NoReturn

from aiogram import Dispatcher

from app.handlers.errors import error_handler


def setup(dispatcher: Dispatcher) -> NoReturn:
    error_handler.setup(dispatcher)
