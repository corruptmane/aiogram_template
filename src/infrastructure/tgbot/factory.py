import structlog
from aiogram import Bot
from aiogram.enums import ParseMode

from .config import BotConfig

log = structlog.get_logger(__name__)


def init_bot(config: BotConfig) -> Bot:
    log.debug('Creating Bot instance')
    return Bot(
        token=config.token,
        session=config.create_session(),
        parse_mode=ParseMode.HTML,
    )
