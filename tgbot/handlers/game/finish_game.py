from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram_dialog import DialogManager, StartMode

from tgbot.misc.states import Main


async def finish_game(_message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(Main.main, mode=StartMode.RESET_STACK)


def register_finish_game(dp: Dispatcher):
    dp.register_message_handler(finish_game, Command("finish_game"))