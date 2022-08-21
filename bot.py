import asyncio
import logging
import ssl
from functools import partial
from typing import Any, Callable

import betterlogging as bl
import sentry_sdk
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import AllowedUpdates, InputFile, ParseMode
from aiogram.utils.executor import start_webhook
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

from app import filters, handlers, middlewares
from app.config import Config
from app.misc.bot_commands import set_bot_commands
from app.services import create_db_engine_and_session_pool

log = logging.getLogger(__name__)


async def webhook_startup(dp: Dispatcher, allowed_updates: list[str], **kwargs) -> None:
    config: Config = kwargs.get('config')
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain('./webhook_cert.pem', './webhook_pkey.pem')
    await dp.bot.delete_webhook()
    await dp.bot.set_webhook(
        config.bot.webhook_url, InputFile('./webhook_cert.pem', 'webhook_cert'),
        allowed_updates=allowed_updates, drop_pending_updates=True
    )
    start_webhook(
        dp, config.bot.webhook_path, skip_updates=True, host='0.0.0.0', port=8443, ssl_context=ssl_context
    )


async def webhook_shutdown(dp: Dispatcher) -> None:
    await dp.bot.delete_webhook()


async def polling_startup(dp: Dispatcher, allowed_updates: list[str], **kwargs) -> None:  # NOQA
    await dp.start_polling(allowed_updates=allowed_updates)


async def polling_shutdown(dp: Dispatcher) -> None: pass  # NOQA


def _pre_configure() -> tuple[Config, int]:
    config = Config.from_env()
    log_level = config.misc.log_level
    bl.basic_colorized_config(level=log_level)
    log.info('Pre-config completed successfully')
    return config, log_level


async def _configure(
        config: Config, log_level: int
) -> tuple[RedisStorage2, Bot, Dispatcher, AsyncEngine, sessionmaker]:
    if config.misc.sentry_dsn is not None:
        sentry_sdk.init(dsn=config.misc.sentry_dsn, integrations=[AioHttpIntegration()])
        log.info('Sentry integration enabled')
    storage = RedisStorage2(host=config.redis.host, port=config.redis.port, password=config.redis.password)
    bot = Bot(config.bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot, storage=storage)
    db_engine, sqlalchemy_session_pool = await create_db_engine_and_session_pool(config.db.sqlalchemy_url, log_level)
    log.info('Objects configured successfully')
    return storage, bot, dp, db_engine, sqlalchemy_session_pool


async def _post_configure(
        config: Config, dp: Dispatcher, bot: Bot, session_pool: sessionmaker
) -> tuple[Callable, Callable]:
    if config.bot.is_webhook:
        startup = webhook_startup
        shutdown = webhook_shutdown
    else:
        startup = polling_startup
        shutdown = polling_shutdown

    allowed_updates: list[str] = [
        *AllowedUpdates.MESSAGE,
        *AllowedUpdates.CALLBACK_QUERY,
        *AllowedUpdates.MY_CHAT_MEMBER,
    ]

    startup = partial(startup, dp, allowed_updates)
    shutdown = partial(shutdown, dp)

    environments: dict[str, Any] = dict(
        config=config
    )

    middlewares.setup(dp, session_pool, .3, environments)
    filters.setup(dp)
    handlers.setup(dp)

    await set_bot_commands(bot, config)
    return startup, shutdown


async def main() -> None:
    config, log_level = _pre_configure()

    storage, bot, dp, db_engine, session_pool = await _configure(config, log_level)

    _startup, _shutdown = await _post_configure(config, dp, bot, session_pool)

    try:
        log.info('Starting bot...')
        await _startup(config=config)
    finally:
        await _shutdown()
        await storage.close()
        await storage.wait_closed()
        await (await bot.get_session()).close()
        await db_engine.dispose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.warning('Bot stopped!')
