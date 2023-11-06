from typing import TypedDict, Any, TYPE_CHECKING

from aiogram import types as tg, Bot, Router
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage
from aiogram.utils.callback_answer import CallbackAnswer
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import Stack, Context
from aiogram_dialog.context.storage import StorageProxy

from src.core.models import dto
from src.infrastructure.db.dao.holder import HolderDAO
from src.tgbot.config import Config

if TYPE_CHECKING:
    from .dialogs import DialogManager


class AiogramMiddlewareData(TypedDict, total=False):
    event_from_user: tg.User
    event_chat: tg.Chat
    bot: Bot
    fsm_storage: BaseStorage
    state: FSMContext
    raw_state: Any
    handler: HandlerObject
    event_update: tg.Update
    event_router: Router
    callback_answer: CallbackAnswer


class DialogMiddlewareData(AiogramMiddlewareData, total=False):
    dialog_manager: DialogManager
    aiogd_storage_proxy: StorageProxy
    aiogd_stack: Stack
    aiogd_context: Context


class MiddlewareData(DialogMiddlewareData, total=False):
    config: Config
    dao: HolderDAO
    user: dto.User | None
