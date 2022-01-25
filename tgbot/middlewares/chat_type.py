from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update, ChatType


class RestrictChatTypesMiddleware(BaseMiddleware):
    def __init__(self, allowed_chat_types: list):
        self.allowed_chat_types = allowed_chat_types
        super().__init__()

    async def on_pre_process_update(self, update: Update, data: dict) -> None:
        allowed_chat_types = self.allowed_chat_types
        if obj := (
                update.message or update.edited_message or update.channel_post or update.edited_channel_post or
                update.callback_query or update.my_chat_member or update.chat_member or update.chat_join_request
        ):
            if obj.chat.type not in allowed_chat_types:
                raise CancelHandler
        elif (update.pre_checkout_query or update.shipping_query) and ChatType.PRIVATE not in allowed_chat_types:
            raise CancelHandler
        elif update.inline_query and (update.inline_query.chat_type not in allowed_chat_types):
            raise CancelHandler
