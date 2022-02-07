from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import ChatType, Update


class RestrictChatTypesMiddleware(BaseMiddleware):
    def __init__(self, allowed_chat_types: list):
        self.allowed_chat_types = allowed_chat_types
        super().__init__()

    async def on_pre_process_update(self, update: Update, data: dict) -> None:
        allowed_types = self.allowed_chat_types
        if update.message and update.message.chat.type not in allowed_types:
            raise CancelHandler()
        if update.edited_message and update.edited_message.chat.type not in allowed_types:
            raise CancelHandler()
        if update.channel_post and update.channel_post.chat.type not in allowed_types:
            raise CancelHandler()
        if update.edited_channel_post and update.edited_channel_post.chat.type not in allowed_types:
            raise CancelHandler()
        if update.callback_query and update.callback_query.message.chat.type not in allowed_types:
            raise CancelHandler()
        if update.my_chat_member and update.my_chat_member.chat.type not in allowed_types:
            raise CancelHandler()
        if update.chat_member and update.chat_member.chat.type not in allowed_types:
            raise CancelHandler()
        if update.chat_join_request and update.chat_join_request.chat.type not in allowed_types:
            raise CancelHandler()
        if update.inline_query and update.inline_query.chat_type not in allowed_types:
            raise CancelHandler()
        if (update.shipping_query or update.pre_checkout_query) and ChatType.PRIVATE not in allowed_types:
            raise CancelHandler()
        # TODO: add processing of poll, poll_answer, chosen_inline_result
