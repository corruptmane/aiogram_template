import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

REF_REGEXP = re.compile(r'.+')


async def ref_start_cmd(msg: Message, state: FSMContext):
    args = msg.get_args()
    await msg.answer(f'Hello, it\'s your args: {args}')
    await state.reset_state()


async def start_cmd(msg: Message, state: FSMContext):
    await msg.answer('Hello')
    await state.reset_state()


def setup(dp: Dispatcher):
    dp.register_message_handler(ref_start_cmd, CommandStart(REF_REGEXP), state='*')
    dp.register_message_handler(start_cmd, CommandStart(), state='*')
