from dataclasses import dataclass, field

from src.infrastructure.db.config import DBConfig
from src.infrastructure.log.config import LoggingConfig
from src.infrastructure.nats.config import NATSConfig
from src.infrastructure.redis.config import RedisConfig
from src.infrastructure.tgbot.config import BotConfig


@dataclass(slots=True, frozen=True)
class Config:
    bot: BotConfig = field(default_factory=BotConfig)
    db: DBConfig = field(default_factory=DBConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)
    nats: NATSConfig = field(default_factory=NATSConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
