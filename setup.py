from aiogram import Dispatcher
from aiogram_dialog import DialogRegistry

# from tgbot.handlers.errors.error_handler import register_error_handler
from tgbot.handlers.game.dialogs import game_dialog
from tgbot.handlers.game.finish_game import register_finish_game
from tgbot.handlers.is_user_active import register_is_active_user
from tgbot.handlers.leaderboard import leaderboard_dialog
from tgbot.handlers.main_dialog import main_dialog
from tgbot.handlers.my_history import my_history_dialog
from tgbot.handlers.settings.settings import settings_dialog
from tgbot.handlers.start import register_start
from tgbot.handlers.test import register_test


def register_all_dialogs(dialog_registry: DialogRegistry):
    dialog_registry.register(main_dialog)
    dialog_registry.register(game_dialog)
    dialog_registry.register(leaderboard_dialog)
    dialog_registry.register(my_history_dialog)
    dialog_registry.register(settings_dialog)


def register_all_handlers(dp: Dispatcher):
    register_finish_game(dp)
    register_start(dp)
    register_test(dp)
    # register_error_handler(dp)
    register_is_active_user(dp)
