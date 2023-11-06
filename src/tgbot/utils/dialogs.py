from abc import abstractmethod

from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager as DialogManager_
from aiogram_dialog.manager.message_manager import MessageManager as MessageManager_
from aiogram_dialog.widgets.input import MessageInput

from .data import MiddlewareData


class DialogManager(DialogManager_):
    @property
    @abstractmethod
    def middleware_data(self) -> MiddlewareData:
        """Middleware data."""
        raise NotImplementedError


class MessageManager(MessageManager_):
    async def answer_callback(
            self, bot: Bot, callback_query: CallbackQuery,
    ) -> None:
        return


async def _unrecognized_input(m: Message, _, __) -> None:
    await m.answer('Sorry, I was not able to understand your request. Please, retry.')


default_input = MessageInput(func=_unrecognized_input)
