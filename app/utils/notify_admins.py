from typing import NoReturn

from aiogram_broadcaster import TextBroadcaster

from app.utils import db_commands


async def notify_admins(action: str) -> NoReturn:
    admins = await db_commands.get_admins()
    chats = [dict(chat_id=admin.user_id, full_name=admin.full_name) for admin in admins]
    if action == "on_startup":
        text = "$full_name, The bot is running!"
    else:
        text = "$full_name, The bot is stopped."
    await TextBroadcaster(chats, text).run()
