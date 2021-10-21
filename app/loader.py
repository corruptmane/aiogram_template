from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import ParseMode
from gino import Gino

from app import config

db = Gino()

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)

storage = RedisStorage2(host=config.REDIS_HOST, port=config.REDIS_PORT)

dp = Dispatcher(bot=bot, storage=storage)

__all__ = ("db", "bot", "storage", "dp")
