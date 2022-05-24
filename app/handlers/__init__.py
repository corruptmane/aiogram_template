import logging

from aiogram import Dispatcher

from app.handlers import error, private

log = logging.getLogger(__name__)


def setup(dp: Dispatcher) -> None:
    error.setup(dp)
    private.setup(dp)
    log.info('Handlers are successfully configured')
