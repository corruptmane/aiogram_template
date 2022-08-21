import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeChat

from app.config import Config

log = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot, config: Config) -> None:
    default_commands = [
        BotCommand('start', 'Restart Bot')
    ]
    await set_default_private_chat_commands(bot, default_commands)
    await set_admin_commands(bot, config.bot.admin_ids, default_commands)
    log.info('Bot commands configured successfully')


async def set_commands_by_chat_ids(bot: Bot, chat_ids: list[int], commands: list[BotCommand]) -> None:
    for chat_id in chat_ids:
        try:
            await bot.set_my_commands(commands, BotCommandScopeChat(chat_id))
        except Exception as e:
            log.error(e)


async def set_default_private_chat_commands(bot: Bot, commands: list[BotCommand]) -> None:
    await bot.set_my_commands(commands, BotCommandScopeAllPrivateChats())


async def set_admin_commands(bot: Bot, admin_ids: tuple[int, ...], default_commands: list[BotCommand]) -> None:
    admin_commands = [
        *default_commands,
        BotCommand('admin', 'Enter admin panel')
    ]
    await set_commands_by_chat_ids(bot, list(admin_ids), admin_commands)
