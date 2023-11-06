from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram_dialog import StartMode

from src.tgbot.state import MenuSG
from src.tgbot.utils.dialogs import DialogManager

router = Router(name='routers.start')


@router.message(F.text == '/start')
async def msg_start_handler(_, state: FSMContext, dialog_manager: DialogManager):
    await state.clear()
    await dialog_manager.start(MenuSG.main, mode=StartMode.RESET_STACK)
