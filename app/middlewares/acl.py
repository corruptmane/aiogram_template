from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.services.repos import UserRepo


class ACLMiddleware(BaseMiddleware):
    allowed_updates = ['message', 'callback_query']

    @staticmethod
    async def setup_chat(data: dict, user: types.User) -> None:
        user_db: UserRepo = data['user_db']
        user_id = user.id
        full_name = user.full_name
        mention = user.get_mention()
        user = await user_db.get_user(user_id)
        if user is None:
            await user_db.add(user_id=user_id, full_name=full_name, mention=mention)
            return
        values = dict()
        if not user.active:
            values.update(active=True)
        if full_name != user.full_name:
            values.update(full_name=full_name)
        if mention != user.mention:
            values.update(mention=mention)
        if values:
            await user_db.update_user(user_id, **values)

    async def on_pre_process_message(self, message: types.Message, data: dict) -> None:
        await self.setup_chat(data, message.from_user)

    async def on_pre_process_callback_query(self, call: types.CallbackQuery, data: dict) -> None:
        await self.setup_chat(data, call.from_user)
