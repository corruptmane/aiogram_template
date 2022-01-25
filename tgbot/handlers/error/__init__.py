from aiogram import Dispatcher

from tgbot.handlers.error import handler


def setup(dp: Dispatcher):
    handler.setup(dp)
