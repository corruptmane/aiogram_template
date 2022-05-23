from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ChatMemberUpdated, Message

from app.services.repos import UserRepo


async def unknown_action(upd: Message | CallbackQuery):
    answer = upd.answer if isinstance(upd, Message) else upd.message.answer
    await answer('Unknown action. Please try again, or type command /start to run steps again')


async def my_chat_member_updated(member: ChatMemberUpdated, state: FSMContext, user_db: UserRepo):
    if not member.new_chat_member.is_chat_member():
        await user_db.not_active_user(member.from_user.id)
        await state.finish()


def setup(dp: Dispatcher):
    dp.register_my_chat_member_handler(my_chat_member_updated, state='*')
    dp.register_message_handler(unknown_action, state='*')
    dp.register_callback_query_handler(unknown_action, state='*')
