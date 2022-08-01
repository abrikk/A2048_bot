from aiogram import Dispatcher
from aiogram_dialog import DialogRegistry

# from tgbot.handlers.errors.error_handler import register_error_handler
from tgbot.handlers.main_dialog import main_dialog
from tgbot.handlers.start import register_start


def register_all_dialogs(dialog_registry: DialogRegistry):
    dialog_registry.register(main_dialog)


def register_all_handlers(dp: Dispatcher):
    register_start(dp)
    # register_error_handler(dp)
