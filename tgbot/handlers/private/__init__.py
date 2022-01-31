from aiogram import Dispatcher

from tgbot.handlers.private import exit, start


def setup(dp: Dispatcher):
    start.setup(dp)
    exit.setup(dp)
