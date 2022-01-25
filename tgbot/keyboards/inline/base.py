from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

back_btn = InlineKeyboardButton('« Back', callback_data='back')
next_btn = InlineKeyboardButton('Next »', callback_data='next')
exit_btn = InlineKeyboardButton('Exit', callback_data='exit')

back_kb = InlineKeyboardMarkup(1, [[back_btn]])
exit_kb = InlineKeyboardMarkup(1, [[exit_btn]])
navigate_kb = InlineKeyboardMarkup(2, [[back_btn, next_btn]])
back_or_exit_kb = InlineKeyboardMarkup(1, [[back_btn], [exit_btn]])
navigate_or_exit_kb = InlineKeyboardMarkup(2, [[back_btn, next_btn], [exit_btn]])


__all__ = (
    'back_btn', 'next_btn', 'exit_btn', 'back_kb', 'exit_kb', 'navigate_kb', 'back_or_exit_kb', 'navigate_or_exit_kb',
    'InlineKeyboardButton', 'InlineKeyboardMarkup', 'CallbackData'
)
