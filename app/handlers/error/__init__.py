from aiogram import Dispatcher

from app.handlers.error import all


def setup(dp: Dispatcher) -> None:
    all.setup(dp)
