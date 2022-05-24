import logging
from dataclasses import dataclass

from environs import Env
from sqlalchemy.engine import URL


@dataclass
class DbConfig:
    host: str
    user: str
    password: str
    database: str

    @property
    def sqlalchemy_url(self) -> URL:
        return URL.create(
            'postgresql+asyncpg',
            username=self.user,
            password=self.password,
            host=self.host,
            port=5432,
            database=self.database
        )


@dataclass
class RedisConfig:
    host: str


@dataclass
class TgBot:
    token: str
    admin_ids: tuple[int, ...]
    is_webhook: bool
    webhook_url: str | None
    webhook_path: str | None


@dataclass
class Miscellaneous:
    log_level: int


@dataclass
class Config:
    bot: TgBot
    db: DbConfig
    redis: RedisConfig
    misc: Miscellaneous

    @classmethod
    def from_env(cls, path: str = None) -> 'Config':
        env = Env()
        env.read_env(path)

        bot_token = env.str('BOT_TOKEN')
        tgbot_config = {
            'token': bot_token,
            'admin_ids': tuple(map(int, env.list('ADMIN_IDS'))),
            'is_webhook': env.bool('IS_WEBHOOK', False),
            'webhook_url': None,
            'webhook_path': None
        }
        if tgbot_config['is_webhook']:
            webhook_host = env.str('WEBHOOK_HOST')
            webhook_path = f'/webhook/{bot_token}'
            webhook_url = f'https://{webhook_host}:8443{webhook_path}'
            tgbot_config.update(webhook_url=webhook_url, webhook_path=webhook_path)

        return cls(
            bot=TgBot(**tgbot_config),
            db=DbConfig(
                host=env.str('DB_HOST', 'postgres'),
                user=env.str('DB_USER', 'postgres'),
                password=env.str('DB_PASSWORD', 'postgres'),
                database=env.str('DB_DATABASE', 'postgres'),
            ),
            redis=RedisConfig(
                host=env.str('REDIS_HOST', 'localhost'),
            ),
            misc=Miscellaneous(
                log_level=env.log_level('LOG_LEVEL', logging.INFO),
            )
        )

