from aiogram.utils.markdown import hcode
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Start, Row, Next, Back
from aiogram_dialog.widgets.text import Format, Const

from tgbot.constants import FOUR_BY_FOUR, FIVE_BY_FIVE, SIX_BY_SIX, SEVEN_BY_SEVEN
from tgbot.handlers.game.getters import good_luck
from tgbot.misc.states import Main, Game, Leaderboard, MyGameHistory, Settings

# The intro logo
logo = hcode("""
╭━━━┳━━━┳╮╱╭┳━━━╮
┃╭━╮┃╭━╮┃┃╱┃┃╭━╮┃
╰╯╭╯┃┃┃┃┃╰━╯┃╰━╯┃
╭━╯╭┫┃┃┃┣━━╮┃╭━╮┃
┃┃╰━┫╰━╯┃╱╱┃┃╰━╯┃
╰━━━┻━━━╯╱╱╰┻━━━╯""".replace("\n", "", 1))


async def get_main_text(dialog_manager: DialogManager, **_kwargs):
    text = (f"{logo}\n\n"
            f"Welcome to the <b>2048 game</b>. To start the game press to the <b>«New game»</b> "
            f"button and choose the size of the game board.\n\n"
            f"- <i>This bot was inspired by the game https://t.me/another_2048_bot</i>")

    return {"main_text": text}


main_dialog = Dialog(
    Window(
        Format(text="{main_text}", when="main_text"),
        Next(
            text=Const("🟢 New game"),
        ),
        Start(
            text=Const("📈 Leaderboard"),
            id="leaderboard",
            state=Leaderboard.main,
            mode=StartMode.RESET_STACK
        ),
        Start(
            text=Const("🌀 Game history"),
            id="history",
            state=MyGameHistory.main,
            mode=StartMode.RESET_STACK
        ),
        Start(
            text=Const("⚙️ Settings"),
            id="settings",
            state=Settings.main,
            mode=StartMode.RESET_STACK
        ),
        disable_web_page_preview=True,
        state=Main.main,
        getter=get_main_text
    ),
    Window(
        Const("To start the game, choose the size of the board below.\n\n"),
        Row(
            Start(
                text=Const("4x4"),
                id=FOUR_BY_FOUR,
                state=Game.on,
                data={"board_size": 4},
                on_click=good_luck,
                mode=StartMode.RESET_STACK
            ),
            Start(
                text=Const("5x5"),
                id=FIVE_BY_FIVE,
                state=Game.on,
                data={"board_size": 5},
                on_click=good_luck,
                mode=StartMode.RESET_STACK
            ),
            Start(
                text=Const("6x6"),
                id=SIX_BY_SIX,
                state=Game.on,
                data={"board_size": 6},
                on_click=good_luck,
                mode=StartMode.RESET_STACK
            ),
            Start(
                text=Const("7x7"),
                id=SEVEN_BY_SEVEN,
                state=Game.on,
                data={"board_size": 7},
                on_click=good_luck,
                mode=StartMode.RESET_STACK
            ),
        ),
        Back(text=Const("🔙 Back")),
        state=Main.new_game
    )
)
