import logging
from typing import NoReturn

from aiogram import Dispatcher

# from app.filters import roles


def setup(dispatcher: Dispatcher) -> NoReturn:
    # dispatcher.filters_factory.bind(roles.IsAdmin)
    # dispatcher.filters_factory.bind(roles.IsBanned)
    logging.info("Filters are successfully configured")
