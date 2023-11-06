from typing import Any, NamedTuple

import structlog
from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseStorage, BaseEventIsolation
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder as RedisKeyBuilder
from nats.aio.client import Client as NATSClient
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from src.infrastructure.tgbot.config import StorageType
from src.infrastructure.tgbot.fsm.nats import (
    NATSFSMAdapter,
    DefaultKvNameBuilder, DefaultKeyBuilder as NATSKeyBuilder,
    NATSStorage,
)
from .config import Config
from .handlers import setup_handlers
from .middlewares import setup_middlewares

log = structlog.get_logger(__name__)


class DispatcherStorage(NamedTuple):
    storage: BaseStorage
    events_isolation: BaseEventIsolation


async def init_storage(
        storage_type: StorageType,
        redis: Redis | None = None,
        nats: NATSClient | None = None,
) -> DispatcherStorage:
    await log.adebug('Creating Storage instance for type %s', storage_type)
    match storage_type:
        case StorageType.memory:
            return DispatcherStorage(MemoryStorage(), SimpleEventIsolation())
        case StorageType.redis:
            if redis is None:
                raise ValueError('You have to pass Redis instance to use RedisStorage')
            storage = RedisStorage(redis, key_builder=RedisKeyBuilder(with_bot_id=True, with_destiny=True))
            return DispatcherStorage(storage, storage.create_isolation())
        case StorageType.nats:
            if nats is None:
                raise ValueError('You have to pass NATS client instance to use NATSStorage')
            adapter = NATSFSMAdapter(nats, kv_name_builder=DefaultKvNameBuilder(), manual_close=True)
            await adapter.create_kv()
            storage = NATSStorage(adapter, key_builder=NATSKeyBuilder(with_bot_id=True, with_destiny=True))
            return DispatcherStorage(storage, SimpleEventIsolation())
        case _:
            raise NotImplementedError


def init_only_dispatcher(storage: DispatcherStorage, **workflow_kwargs: Any) -> Dispatcher:
    log.debug('Creating Dispatcher instance')
    return Dispatcher(
        storage=storage.storage,
        events_isolation=storage.events_isolation,
        **workflow_kwargs,
    )


async def init_dispatcher(
        config: Config,
        redis: Redis | None = None,
        nats: NATSClient | None = None,
        **workflow_kwargs: Any,
) -> Dispatcher:
    storage = await init_storage(config.bot.storage_type, redis, nats)
    dp = init_only_dispatcher(storage, **workflow_kwargs)
    return dp


def setup_shutdown_events(dp: Dispatcher, db_engine: AsyncEngine, redis: Redis) -> None:
    dp.shutdown.register(db_engine.dispose)
    dp.shutdown.register(redis.close)


def setup_events(
        dp: Dispatcher, *, db_engine: AsyncEngine, config: Config,
        session_factory: async_sessionmaker[AsyncSession], redis: Redis,
) -> None:
    setup_middlewares(
        dp,
        session_factory=session_factory, config=config, redis=redis,
    )
    setup_handlers(dp)
    setup_shutdown_events(dp, db_engine, redis)
