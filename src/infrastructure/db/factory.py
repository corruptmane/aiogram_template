from typing import Any

import orjson
import structlog
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from src.core.utils.json import JsonLoads, JsonDumps, orjson_dumps
from src.infrastructure.db.config import DBConfig

log = structlog.get_logger(__name__)


def init_sqlalchemy_engine(
        cfg: DBConfig,
        query_cache_size: int = 1200,
        pool_size: int = 100,
        max_overflow: int = 200,
        json_deserializer: JsonLoads = orjson.loads,
        json_serializer: JsonDumps = orjson_dumps,
        **engine_kwargs: Any,
) -> AsyncEngine:
    log.debug('Creating SQLAlchemy Engine instance')
    return create_async_engine(
        cfg.url,
        query_cache_size=query_cache_size,
        pool_size=pool_size,
        max_overflow=max_overflow,
        json_deserializer=json_deserializer,
        json_serializer=json_serializer,
        **engine_kwargs,
    )


def init_sqlalchemy_session_factory(
        engine: AsyncEngine,
        expire_on_commit: bool = False,
) -> async_sessionmaker[AsyncSession]:
    log.debug('Creating SQLAlchemy Session Factory (sessionmaker)')
    return async_sessionmaker(bind=engine, expire_on_commit=expire_on_commit, class_=AsyncSession)
