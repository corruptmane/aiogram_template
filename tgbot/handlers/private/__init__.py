from aiogram import Dispatcher

from tgbot.handlers.private import start, exit


def setup(dp: Dispatcher):
    start.setup(dp)
    exit.setup(dp)
