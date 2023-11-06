from aiogram import Router
from aiogram_dialog import setup_dialogs as install_dialogs

from src.tgbot.utils.dialogs import MessageManager
from . import error, start, dialogs


def setup_handlers(router: Router) -> None:
    router.include_routers(
        error.router,
        start.router,
        *dialogs.all_dialogs,
    )
    install_dialogs(router, message_manager=MessageManager())
