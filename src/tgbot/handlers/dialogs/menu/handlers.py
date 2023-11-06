import structlog
from aiogram.types import CallbackQuery

from src.tgbot.utils.dialogs import DialogManager

log = structlog.get_logger(__name__)


# noinspection PyUnusedLocal
async def close_main_menu_dialog(c: CallbackQuery, _, dm: DialogManager) -> None:
    await log.ainfo('Closing main menu dialog')
    await dm.done()
