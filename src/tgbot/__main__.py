import asyncio
from typing import Never

import structlog

from src.common import get_app_dir_path, Paths
from src.infrastructure.config_loader import load_config
from src.infrastructure.db.factory import init_sqlalchemy_engine, init_sqlalchemy_session_factory
from src.infrastructure.log.main import configure_logging
from src.infrastructure.nats.factory import init_nats_adapter
from src.infrastructure.redis.factory import init_redis
from src.infrastructure.tgbot.factory import init_bot
from .config import Config
from .factory import init_dispatcher, setup_events

log = structlog.get_logger(__name__)


async def main() -> Never:
    paths = Paths(app_dir=get_app_dir_path())
    config = load_config(Config, path=paths.config_file_path)
    configure_logging(config.logging)

    bot = init_bot(config.bot)
    redis = init_redis(config.redis)
    db_engine = init_sqlalchemy_engine(config.db)
    session_factory = init_sqlalchemy_session_factory(db_engine, expire_on_commit=True)

    if config.bot.skip_updates:
        await bot.delete_webhook(drop_pending_updates=True)

    async with (
        init_nats_adapter(config.nats) as nats_adapter,
    ):
        dp = await init_dispatcher(config, redis, nats_adapter.client)
        setup_events(
            dp, db_engine=db_engine, config=config, session_factory=session_factory, redis=redis,
        )

        await log.ainfo('Running Telegram Bot')

        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


def run() -> Never:
    asyncio.run(main())


if __name__ == '__main__':
    run()
