import logging
from typing import NoReturn

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats

from tgbot.config import Config

log = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot, config: Config) -> NoReturn:
    default_commands = {
        'en': [
            BotCommand('start', '[Re]Start Bot'),
        ],
        'ru': [
            BotCommand('start', '[Ре]Старт Бота'),
        ]
    }
    await set_private_chat_commands(bot, default_commands)
    await set_admin_commands(bot, config.bot.admin_ids, default_commands)
    log.info('Bot commands configured successfully')


async def set_private_chat_commands(bot: Bot, default_commands: dict[str, list[BotCommand]]) -> NoReturn:
    for lang, commands in default_commands.items():
        await bot.set_my_commands(commands, BotCommandScopeAllPrivateChats(), lang)
    await bot.set_my_commands(default_commands['en'], BotCommandScopeAllPrivateChats())


async def set_admin_commands(
        bot: Bot, admin_ids: tuple[int, ...], default_commands: dict[str, list[BotCommand]]
) -> NoReturn:
    lang_commands = {
        'en': [
            *default_commands['en'],
            BotCommand('admin', 'Enter admin panel'),
        ],
        'ru': [
            *default_commands['ru'],
            BotCommand('admin', 'Войти в админ-панель')
        ]
    }
    for admin_id in admin_ids:
        for lang, commands in lang_commands.items():
            await bot.set_my_commands(commands, BotCommandScopeChat(admin_id), lang)
        await bot.set_my_commands(lang_commands['en'], BotCommandScopeChat(admin_id))
