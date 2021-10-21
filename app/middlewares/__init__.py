import logging
from typing import NoReturn

from aiogram import Dispatcher


def setup(dispatcher: Dispatcher) -> NoReturn:
    # dispatcher.setup_middleware()
    logging.info("Middlewares are successfully configured")
