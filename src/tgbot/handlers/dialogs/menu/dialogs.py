from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const

from .getters import main_menu_getter
from src.tgbot.state import MenuSG
from .handlers import close_main_menu_dialog

dialog = Dialog(

    Window(
        Format('Main menu\n\nYour full name is: <code>{full_name}</code>'),
        Button(
            text=Const('Exit main menu'),
            id='cancel',
            on_click=close_main_menu_dialog,
        ),
        state=MenuSG.main,
        getter=main_menu_getter,
    ),

)
