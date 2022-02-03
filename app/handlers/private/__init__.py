from aiogram import Dispatcher

from app.handlers.private import exit, start


def setup(dp: Dispatcher):
    start.setup(dp)
    exit.setup(dp)
