from aiogram.utils.markdown import hcode, hlink
from aiogram_dialog import Dialog, Window, StartMode, DialogManager
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format, Const

from tgbot.misc.states import Leaderboard, Main
from tgbot.models.game_history import GameHistory
from tgbot.services.db_commands import DBCommands

leaderboard_logo = hcode("""
   __               __       
  / /  ___ ___ ____/ /__ ____
 / /__/ -_) _ `/ _  / -_) __/
/____/\__/\_,_/\_,_/\__/_/   
   ___                   __  
  / _ )___  ___ ________/ /  
 / _  / _ \/ _ `/ __/ _  /   
/____/\___/\_,_/_/  \_,_/    
                             
""".replace("\n", "", 1))

rank_emojies: dict = {
    1: hcode("🏆 ①"),
    2: hcode("🥈 ②"),
    3: hcode("🥉 ③"),
    4: hcode("🎖 ④"),
    5: hcode("🏅 ⑤"),
}


def get_user_mention(id: int, full_name: str, last_name: str = None, username: str = None) -> str:
    name = last_name and " ".join([full_name, last_name]) or full_name
    if username:
        return hlink(name, f"t.me/{username}")
    else:
        return hlink(name, f"tg://user?id={id}")


async def get_user_rank(mention: str, game_history: GameHistory, rank: int):
    rankt: str = rank_emojies.get(rank)
    size = f"{game_history.board_size}x{game_history.board_size}"
    text = (f"{rankt} {mention}:\n"
            f"<code>\t  score: {game_history.score}\n"
            f"\tsize: {size}\n"
            f"\tmoves made: {game_history.moves_made}\n"
            f"\tthe biggest number: {game_history.max_num}\n"
            f"\tplayed at: {game_history.created_at.strftime('%d.%m.%Y')}</code>").expandtabs(4)

    return text


async def get_leaderboard_text(dialog_manager: DialogManager, **_kwargs):
    db: DBCommands = dialog_manager.data.get("db_commands")
    game_history = await db.get_game_history()
    dialog_manager.event.from_user.get_mention()
    text = f"{leaderboard_logo}\n"

    if game_history:
        for rank, game_history in game_history:
            text += await get_user_rank(dialog_manager.event.from_user.mention, game_history, rank) + "\n\n"

    else:
        text += "No games yet"

    return {"leaderboard_text": text}


leaderboard_dialog = Dialog(
    Window(
        Format(text="{leaderboard_text}", when="leaderboard_text"),
        Start(
            text=Const("🔙 Back"),
            id="to_main",
            state=Main.main,
            mode=StartMode.RESET_STACK
        ),
        state=Leaderboard.main,
        getter=get_leaderboard_text,
        disable_web_page_preview=True
    )
)
