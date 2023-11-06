import structlog
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from .config import RedisConfig

log: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


def init_redis_connection_pool(url: str) -> ConnectionPool:
    log.debug('Creating Redis connection pool')
    return ConnectionPool.from_url(url)


def init_redis(config: RedisConfig) -> Redis:
    log.debug('Creating Redis instance')
    return Redis(
        connection_pool=init_redis_connection_pool(config.url),
    )
