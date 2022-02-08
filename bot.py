import asyncio
import logging
import ssl

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import AllowedUpdates, ChatType, InputFile
from aiogram.utils.executor import start_webhook

from app import filters, handlers, middlewares
from app.config import Config, load_config
from app.misc import set_bot_commands
from app.services import create_db_engine_and_session_pool

log = logging.getLogger(__name__)


async def webhook_startup(dp: Dispatcher, allowed_updates: list[str], **kwargs):
    config: Config = kwargs.get('config')
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.load_cert_chain('./webhook_cert.pem', './webhook_pkey.pem')
    await dp.bot.delete_webhook(True)
    await dp.bot.set_webhook(
        config.bot.webhook_url, InputFile('./webhook_cert.pem', 'webhook_cert'),
        allowed_updates=allowed_updates, drop_pending_updates=True
    )
    start_webhook(
        dp, config.bot.webhook_path, skip_updates=True, host='0.0.0.0', port=8443, ssl_context=ssl_context
    )


async def webhook_shutdown(dp: Dispatcher):
    await dp.bot.delete_webhook(True)


async def polling_startup(dp: Dispatcher, allowed_updates: list[str], **kwargs):
    await dp.start_polling(allowed_updates=allowed_updates)


async def polling_shutdown(dp: Dispatcher): pass


async def main():
    config: Config = load_config()
    logging.basicConfig(
        level=config.misc.log_level,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    log.info('Starting bot...')

    storage = RedisStorage2(
        host=config.redis.host, port=6379, password=config.redis.password if config.redis.password else None
    )
    bot = Bot(config.bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    db_engine, sqlalchemy_session_pool = await create_db_engine_and_session_pool(config)

    startup = webhook_startup if config.bot.is_webhook else polling_startup
    shutdown = webhook_shutdown if config.bot.is_webhook else polling_shutdown
    allowed_updates: list[str] = AllowedUpdates.MESSAGE + AllowedUpdates.CALLBACK_QUERY + AllowedUpdates.MY_CHAT_MEMBER

    bot['config'] = config

    middlewares.setup(dp, ChatType.PRIVATE, sqlalchemy_session_pool, .3)
    filters.setup(dp)
    handlers.setup(dp)

    await set_bot_commands(bot, config)

    try:
        await startup(dp, allowed_updates, config=config)
    finally:
        await shutdown(dp)
        await storage.close()
        await storage.wait_closed()
        bot_session = await dp.bot.get_session()
        await bot_session.close()
        await db_engine.dispose()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.warning('Bot stopped!')
