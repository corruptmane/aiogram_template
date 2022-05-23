import logging

from aiogram import Dispatcher

from app.filters.is_admin import IsAdmin

log = logging.getLogger(__name__)


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin, event_handlers=[dp.message_handlers, dp.callback_query_handlers])
    log.info('Filters are successfully configured')
