import logging

from aiogram import Dispatcher

from tgbot.filters.is_admin import IsAdmin

log = logging.getLogger(__name__)


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)
    log.info('Filters are successfully configured')
