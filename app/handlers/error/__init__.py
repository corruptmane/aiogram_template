from aiogram import Dispatcher

from app.handlers.error import handler


def setup(dp: Dispatcher):
    handler.setup(dp)
