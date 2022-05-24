from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from app.misc.regex import REF_REGEXP


async def ref_start_cmd(msg: Message, state: FSMContext):
    args = msg.get_args()
    await msg.answer(f'Hello, it\'s your args: {args}')
    await state.finish()


async def start_cmd(msg: Message, state: FSMContext):
    await msg.answer('Hello')
    await state.finish()


def setup(dp: Dispatcher) -> None:
    dp.register_message_handler(ref_start_cmd, CommandStart(REF_REGEXP), state='*')
    dp.register_message_handler(start_cmd, CommandStart(), state='*')
