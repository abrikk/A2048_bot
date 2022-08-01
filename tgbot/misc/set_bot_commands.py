import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat
from aiogram.utils.exceptions import ChatNotFound, BotBlocked

from tgbot.config import Config


async def set_default_commands(bot: Bot, config: Config):
    usercommands = [
        BotCommand(command="start", description="Start bot"),
        BotCommand(command="help", description="Help")
    ]
    await bot.set_my_commands(usercommands, scope=BotCommandScopeDefault())

    admin_commands = [
        BotCommand(command="start", description="Start bot"),
        BotCommand(command="help", description="Help")
    ]
    try:
        for admin in config.tg_bot.admin_ids:
            await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin))
    except ChatNotFound:
        logging.warning("Forbidden: Chat not found")
    except BotBlocked:
        logging.warning("Forbidden: bot was blocked by the user")
