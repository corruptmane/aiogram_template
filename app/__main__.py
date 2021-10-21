from typing import NoReturn

from aiogram import Dispatcher
from aiogram.utils import executor

from app import config, filters, handlers, middlewares, misc, utils
from app.loader import dp
from app.models import base


async def on_startup(dispatcher: Dispatcher) -> NoReturn:
    handlers.setup(dispatcher)
    middlewares.setup(dispatcher)
    filters.setup(dispatcher)
    await base.connect(config.POSTGRES_URI)
    await utils.setup_default_commands(dispatcher)
    # await utils.notify_admins('on_startup')


async def on_shutdown(dispatcher: Dispatcher) -> NoReturn:
    # await utils.notify_admins('on_shutdown')
    await base.close_connection()


if __name__ == "__main__":
    utils.setup_logger(config.LOGGING_LEVEL, ["sqlalchemy.engine", "aiogram.bot.api"])
    executor.start_polling(
        dp,
        skip_updates=config.SKIP_UPDATES,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )
