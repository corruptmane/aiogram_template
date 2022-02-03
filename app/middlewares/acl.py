from typing import NoReturn

from aiogram import types
from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.models import User
from app.services import DatabaseContext


class ACLMiddleware(BaseMiddleware):
    allowed_updates = ['message', 'callback_query']

    @staticmethod
    async def setup_chat(data: dict, user: types.User) -> NoReturn:
        user_db: DatabaseContext[User] = data['user_db']
        user_id = user.id
        full_name = user.full_name
        mention = user.get_mention()
        if not await user_db.exists(User.user_id == user_id):
            await user_db.add(user_id=user_id, full_name=full_name, mention=mention, active=True)
        else:
            await user_db.update(User.user_id == user_id, full_name=full_name, mention=mention)

    async def on_pre_process_message(self, message: types.Message, data: dict) -> NoReturn:
        await self.setup_chat(data, message.from_user)

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict) -> NoReturn:
        await self.setup_chat(data, call.from_user)

    @staticmethod
    async def on_post_process_callback_query(call: types.CallbackQuery, data: dict) -> NoReturn:
        handler = current_handler.get()
        if not handler or not getattr(handler, 'answered_cb', False):
            await call.answer()
