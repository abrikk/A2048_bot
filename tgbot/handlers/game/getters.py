from aiogram import types
from aiogram.utils.markdown import hcode
from aiogram_dialog import DialogManager
import numpy as np
from aiogram_dialog.widgets.kbd import Select, Button
from aiogram_dialog.widgets.managed import ManagedWidgetAdapter

from tgbot.constants import VITALII_THEME, CLASSIC_THEME
from tgbot.handlers.game.exceptions import BoardNotModifiedError
from tgbot.handlers.game.logic import get_start_board, convert_matrix_to_dict, prepare_board, get_actions, \
    move_number_fields, convert_dict_to_matrix, is_game_over, num_to_emoji
from tgbot.handlers.game.vitalii_theme.draw_table import draw_table
from tgbot.models.game_history import GameHistory
from tgbot.models.user import User


async def set_random_fields(_, dialog_manager: DialogManager):
    start_data = dialog_manager.current_context().start_data
    dialog_data = dialog_manager.current_context().dialog_data

    boards_size: int = start_data.get("board_size")
    board: np.ndarray = get_start_board(boards_size)

    dialog_data.update(convert_matrix_to_dict(board))
    dialog_data.update({"score": 0, "game_over": False, "max_num": np.amax(board), "moves_made": 0})


async def get_game_data(dialog_manager: DialogManager, **_kwargs):
    session = dialog_manager.data.get("session")
    user: User = await session.get(User, dialog_manager.event.from_user.id)
    dialog_data = dialog_manager.current_context().dialog_data
    game_over = dialog_data.get("game_over", False)
    score = dialog_data.get("score", 0)
    max_num = dialog_data.get("max_num")
    moves_made = dialog_data.get("moves_made", 0)

    game_text = f"⚜️ The biggest number: {num_to_emoji(max_num)} \n\n" \
                f"💬 Moves made: {moves_made}\n\n" \
                f"🔥 Score: {score}"

    if user.theme == VITALII_THEME:
        game_text += "\n\n" + hcode(draw_table(convert_dict_to_matrix(prepare_board(dialog_data, user.numbers_style))))

    if game_over:
        game_text += "\n\n❗️ Game over ❗️"

    return {"game_text": game_text, "game_over": game_over, "classic_theme": user.theme == CLASSIC_THEME,
            **prepare_board(dialog_data, user.numbers_style), **get_actions(user.controllers)}


async def move_numbers(_call: types.CallbackQuery, _widget: ManagedWidgetAdapter[Select], manager: DialogManager,
                       direction: str):
    if direction == "empty":
        return

    dialog_data = manager.current_context().dialog_data

    try:
        moving, score = move_number_fields(
            array=convert_dict_to_matrix(dialog_data),
            score=dialog_data.get('score', 0),
            direction=direction
        )
    except BoardNotModifiedError:
        return

    if not isinstance(moving, bool):
        dialog_data.update(convert_matrix_to_dict(moving))
        dialog_data["score"] = score
        dialog_data["max_num"] = np.amax(moving)
        dialog_data["moves_made"] += 1

    if moving is False or is_game_over(moving):
        start_data = manager.current_context().start_data
        boards_size: int = start_data.get("board_size")
        session = manager.data.get("session")
        dialog_data["game_over"] = True
        obj = manager.event
        moves_made = dialog_data["moves_made"]

        game_history: GameHistory = GameHistory(
            user_id=obj.from_user.id,
            board_size=boards_size,
            score=score,
            moves_made=moves_made,
            max_num=dialog_data["max_num"]
        )

        session.add(game_history)
        await session.commit()


async def good_luck(call: types.CallbackQuery, _button: Button, _manager: DialogManager):
    await call.answer("💪 Good luck! 💪")
