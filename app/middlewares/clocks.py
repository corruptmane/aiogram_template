from typing import Callable

from aiogram import types
from aiogram.dispatcher.handler import current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware


class ClocksMiddleware(BaseMiddleware):

    @staticmethod
    async def setup_chat(handler: Callable, data: dict, chat: types.Chat):
        if hasattr(handler, 'clocks'):
            return
        chat_id = int(chat.id)
        msg = await chat.bot.send_message(chat_id, '⏳')
        await chat.bot.send_chat_action(chat_id, 'typing')

        data['clocks_msg'] = msg

    @staticmethod
    async def close_chat(data: dict):
        if msg := data.get('clocks_msg', None):
            await msg.delete()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        await self.setup_chat(handler, data, message.chat)

    async def on_process_callback_query(self, call: types.CallbackQuery, data: dict):
        handler = current_handler.get()
        await self.setup_chat(handler, data, call.message.chat if call.message else None)

    async def on_post_process_message(self, message: types.Message, args: list, data: dict):
        await self.close_chat(data)

    async def on_post_process_callback_query(self, call: types.CallbackQuery, args: list, data: dict):
        handler = current_handler.get()
        await self.close_chat(data)
        if handler and not hasattr(handler, 'answered'):
            await call.answer()
