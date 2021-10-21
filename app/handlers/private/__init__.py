from typing import NoReturn

from aiogram import Dispatcher

from app.handlers.private import echo, start


def setup(dispatcher: Dispatcher) -> NoReturn:
    start.setup(dispatcher)
    echo.setup(dispatcher)
