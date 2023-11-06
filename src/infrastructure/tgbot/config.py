from dataclasses import dataclass, field
from enum import Enum

import orjson
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from src.core.utils.json import JsonLoads, JsonDumps, orjson_dumps


class StorageType(str, Enum):
    memory = 'memory'
    redis = 'redis'
    nats = 'nats'


@dataclass(slots=True, frozen=True)
class BotConfig:
    token: str
    admin_ids: list[int] = field(default_factory=list)
    storage_type: StorageType = StorageType.memory
    parse_mode: ParseMode = ParseMode.HTML
    skip_updates: bool = False

    @staticmethod
    def create_session(
            json_loads: JsonLoads = orjson.loads,
            json_dumps: JsonDumps = orjson_dumps,
    ) -> AiohttpSession:
        return AiohttpSession(
            json_loads=json_loads,
            json_dumps=json_dumps,
        )
