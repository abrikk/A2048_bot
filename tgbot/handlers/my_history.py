from aiogram.utils.markdown import hcode
from aiogram_dialog import Dialog, Window, StartMode, DialogManager
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format, Const

from tgbot.misc.states import MyGameHistory, Main
from tgbot.models.game_history import GameHistory
from tgbot.services.db_commands import DBCommands


def get_hist_text(history: GameHistory) -> str:
    print(history)
    text = (f"• Game played at {history.created_at.strftime('%d.%m.%Y')}\n"
            f"\t\t- score: {history.score}\n"
            f"\t\t- size: {history.board_size}x{history.board_size}\n"
            f"\t\t-moves made: {history.moves_made}\n"
            f"\t\t-the biggest number: {history.max_num}\n")

    return hcode(text)


async def get_my_history_text(dialog_manager: DialogManager, **_kwargs):
    db: DBCommands = dialog_manager.data.get("db_commands")
    last_games: list[GameHistory] = await db.get_user_history(dialog_manager.event.from_user.id)
    print(last_games)
    if not last_games:
        return {"my_history_text": (f"🌀 ＧＡＭＥ ＨＩＳＴＯＲＹ 🌀\n\n"
                                    f"You haven't played any games yet.")}

    last_games_text: str = '\n\n'.join([get_hist_text(game) for game in last_games])
    best_game: GameHistory = await db.get_best_user_game(dialog_manager.event.from_user.id)

    text = (
            f"The most well-played game:\n"
            f"{get_hist_text(best_game)}\n\n"
            f"The last games:\n"
            f"{last_games_text}")

    return {"my_history_text": text}

my_history_dialog = Dialog(
    Window(
        Format(text="{my_history_text}", when="my_history_text"),
        Start(
            text=Const("🔙 Back"),
            id="to_main",
            state=Main.main,
            mode=StartMode.RESET_STACK
        ),
        state=MyGameHistory.main,
        getter=get_my_history_text
    )
)
