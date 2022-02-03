from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ChatMemberUpdated, Message

from app.models import User
from app.services import DatabaseContext


async def unknown_action(upd: Message | CallbackQuery):
    answer = upd.answer if isinstance(upd, Message) else upd.message.answer
    await answer('Unknown action. Please try again, or type command /start to run steps again')


async def my_chat_member_updated(member: ChatMemberUpdated, state: FSMContext, user_db: DatabaseContext[User]):
    if not member.new_chat_member.is_chat_member():
        await user_db.update(User.user_id == member.from_user.id, active=False)
        await state.reset_state()


def setup(dp: Dispatcher):
    dp.register_my_chat_member_handler(my_chat_member_updated, state='*')
