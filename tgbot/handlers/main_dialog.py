from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Start, Row
from aiogram_dialog.widgets.text import Format, Const

from tgbot.constants import FOUR_BY_FOUR, FIVE_BY_FIVE, SIX_BY_SIX, SEVEN_BY_SEVEN
from tgbot.misc.states import Main, Game
from tgbot.models.user import User


async def get_main_text(dialog_manager: DialogManager, **_kwargs):
    start_data = dialog_manager.current_context().start_data
    if start_data:
        first_name = start_data.get("first_name")
    else:
        user: User = dialog_manager.data.get("user")
        first_name = user.first_name

    text = (f"Hello, {first_name}!\n\n"
            f"To start the game, choose the size of the board below.\n\n"
            f"- <i>This bot was inspired by the game https://t.me/another_2048_bot</i>")

    return {"main_text": text}


main_dialog = Dialog(
    Window(
        Format(text="{main_text}", when="main_text"),
        Row(
            Start(
                text=Const("4x4"),
                id=FOUR_BY_FOUR,
                state=Game.on
            ),
            Start(
                text=Const("5x5"),
                id=FIVE_BY_FIVE,
                state=Game.on
            ),
            Start(
                text=Const("6x6"),
                id=SIX_BY_SIX,
                state=Game.on
            ),
            Start(
                text=Const("7x7"),
                id=SEVEN_BY_SEVEN,
                state=Game.on
            ),
        ),
        disable_web_page_preview=True,
        state=Main.main,
        getter=get_main_text
    )
)
