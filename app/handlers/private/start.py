from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from app.config import Config


async def start_cmd(msg: Message, state: FSMContext, config: Config):
    # Here, we got `config` with help of `app.middlewares.environment.EnvironmentMiddleware`
    admin_ids = '\n'.join(map(str, config.bot.admin_ids))
    await msg.answer(f'Hello, admin ids are:\n\n{admin_ids}')
    await state.finish()


def setup(dp: Dispatcher) -> None:
    dp.register_message_handler(start_cmd, CommandStart(), state='*')
