import copy

from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hitalic
from aiogram_dialog import Dialog, Window, StartMode, DialogManager
from aiogram_dialog.widgets.kbd import Column, Next, SwitchTo, Start, Row, Button
from aiogram_dialog.widgets.text import Const, Format

from tgbot.constants import VITALII_THEME, CLASSIC_THEME, VITALII_CONTROLLERS, CLASSIC_CONTROLLERS, ROMAN_NUMBERS, \
    EMOJI_NUMBERS, CLASSIC_NUMBERS, MILL_CONTROLLERS
from tgbot.misc.media_widget import DynamicMediaFileId
from tgbot.misc.states import Settings, Main
from tgbot.models.user import User

# red AgACAgIAAxkBAAIEG2Lv5wR9Vhot6gVqQ7vKyVIrckq-AALuvjEbXKuBS9t-7pWvvRXDAQADAgADeAADKQQ
# green AgACAgIAAxkBAAIEHGLv5yWIbK7O4FI9wkJ5nNZ9RkILAALwvjEbXKuBS0SD6eBDfMXjAQADAgADeQADKQQ
# blue AgACAgIAAxkBAAIEHWLv5zcgbyv59GaqubmukQ4VS9ACAALxvjEbXKuBS48GhzwoaL1kAQADAgADeAADKQQ
# vitalii controllers AgACAgIAAxkBAAIElmLwuTFS6BaI_GErogItWyP5OvsGAAJJwDEbhVGIS0uL1D0W5DuMAQADAgADbQADKQQ
# classic controllers AgACAgIAAxkBAAIEmmLwuV3sWbQatmiu8qLFw81I7Hr3AAJKwDEbhVGIS-LHTzci915sAQADAgADbQADKQQ
# mill controllers AgACAgIAAxkBAAIEm2LwuXfrstSf6sdOJkzSs9zk4TE_AAJLwDEbhVGIS20RUXK2yMuiAQADAgADbQADKQQ

photo_theme: dict = {
    CLASSIC_THEME: "AgACAgIAAxkBAAIEHWLv5zcgbyv59GaqubmukQ4VS9ACAALxvjEbXKuBS48GhzwoaL1kAQADAgADeAADKQQ",
    VITALII_THEME: "AgACAgIAAxkBAAIEG2Lv5wR9Vhot6gVqQ7vKyVIrckq-AALuvjEbXKuBS9t-7pWvvRXDAQADAgADeAADKQQ"
}

photo_controllers: dict = {
    CLASSIC_CONTROLLERS: "AgACAgIAAxkBAAIEmmLwuV3sWbQatmiu8qLFw81I7Hr3AAJKwDEbhVGIS-LHTzci915sAQADAgADbQADKQQ",
    VITALII_CONTROLLERS: "AgACAgIAAxkBAAIElmLwuTFS6BaI_GErogItWyP5OvsGAAJJwDEbhVGIS0uL1D0W5DuMAQADAgADbQADKQQ",
    MILL_CONTROLLERS: "AgACAgIAAxkBAAIEm2LwuXfrstSf6sdOJkzSs9zk4TE_AAJLwDEbhVGIS20RUXK2yMuiAQADAgADbQADKQQ"
}

photo_numbers: dict = {
    CLASSIC_NUMBERS: "AgACAgIAAxkBAAIEvWLwvwnQYZ9k4Swe-x6IQBSKV6H7AAJdwDEbhVGIS25hbfeD9Lr1AQADAgADbQADKQQ",
    EMOJI_NUMBERS: "AgACAgIAAxkBAAIEvGLwvszs74HK1PQXZEBXtgG8bh6PAAJcwDEbhVGIS3V4mxp1ZjedAQADAgADeAADKQQ",
    ROMAN_NUMBERS: "AgACAgIAAxkBAAIEvmLwvyH-5U6Hz5KPJNR9ETi11Fm2AAJfwDEbhVGISx-QkOGWcl9UAQADAgADeAADKQQ"
}

themes: dict = {
    CLASSIC_THEME: "Classic theme",
    VITALII_THEME: "Vitalii theme"
}

controllers: dict = {
    CLASSIC_CONTROLLERS: "Classic controllers",
    VITALII_CONTROLLERS: "Vitalii controllers",
    MILL_CONTROLLERS: "Mill controllers"
}

numbers: dict = {
    CLASSIC_NUMBERS: "Classic numbers",
    EMOJI_NUMBERS: "Emoji numbers",
    ROMAN_NUMBERS: "Roman numbers"
}


async def get_theme_text(dialog_manager: DialogManager, **_kwargs):
    dialog_data = dialog_manager.current_context().dialog_data
    session = dialog_manager.data.get("session")
    user: User = await session.get(User, dialog_manager.event.from_user.id)

    text = f"🧑‍🎤 The current theme that is on the photo is {hitalic(themes.get(user.theme))}.\n\n" \
           f"If you want to change the theme choose another theme of the game:"

    if is_confirming := dialog_data.get("new_theme"):
        text += "\n\nAre you sure you want to change the theme of the game to that is shown on the picture?"
        current_photo_theme = photo_theme.get(dialog_data.get("new_theme"))
    else:
        current_photo_theme = photo_theme.get(user.theme)

    return {"theme_text": text, "photo_theme": current_photo_theme, "confirm_theme": bool(is_confirming)}


async def get_themes(dialog_manager: DialogManager, **_kwargs):
    session = dialog_manager.data.get("session")
    user: User = await session.get(User, dialog_manager.event.from_user.id)

    getter_themes = copy.deepcopy(themes)
    getter_themes[user.theme] = "✅ " + themes.get(user.theme, "")

    return {"game_themes": list(getter_themes.values())}


async def get_controllers_text(dialog_manager: DialogManager, **_kwargs):
    dialog_data = dialog_manager.current_context().dialog_data
    session = dialog_manager.data.get("session")
    user: User = await session.get(User, dialog_manager.event.from_user.id)

    text = f"🕹 The current controllers style is that shown on the photo is {hitalic(controllers.get(user.controllers))}.\n\n" \
           f"If you want to change the controllers style choose another below:"

    if is_confirming := dialog_data.get("new_controllers"):
        text += "\n\nAre you sure you want to change the style of the controllers to that is shown on the picture?"
        current_photo_controllers = photo_controllers.get(dialog_data.get("new_controllers"))
    else:
        current_photo_controllers = photo_controllers.get(user.controllers)

    return {"controllers_text": text, "photo_controllers": current_photo_controllers, "confirm_controllers": bool(is_confirming)}


async def get_controllers(dialog_manager: DialogManager, **_kwargs):
    session = dialog_manager.data.get("session")
    user: User = await session.get(User, dialog_manager.event.from_user.id)

    getter_controllers = copy.deepcopy(controllers)
    getter_controllers[user.controllers] = "✅ " + controllers.get(user.controllers, "")

    return {"game_controllers": list(getter_controllers.values())}


async def get_numbers_text(dialog_manager: DialogManager, **_kwargs):
    dialog_data = dialog_manager.current_context().dialog_data
    session = dialog_manager.data.get("session")
    user: User = await session.get(User, dialog_manager.event.from_user.id)

    text = f"🔢 The current numbers style is that shown on the photo is {hitalic(numbers.get(user.numbers_style))}.\n\n" \
           f"If you want to change the numbers style choose another below:"

    if is_confirming := dialog_data.get("new_number_style"):
        text += "\n\nAre you sure you want to change the style of the numbers to that is shown on the picture?"
        current_photo_numbers = photo_numbers.get(dialog_data.get("new_number_style"))
    else:
        current_photo_numbers = photo_numbers.get(user.numbers_style)

    if EMOJI_NUMBERS in (is_confirming, user.numbers_style):
        text += "\n\n⚠️ <i>WARNING: using this style of numbers you may encounter a problem displaying the game.</i>"

    return {"numbers_text": text, "photo_numbers": current_photo_numbers, "confirm_numbers": bool(is_confirming)}


async def get_numbers(dialog_manager: DialogManager, **_kwargs):
    session = dialog_manager.data.get("session")
    user: User = await session.get(User, dialog_manager.event.from_user.id)

    getter_numbers = copy.deepcopy(numbers)
    getter_numbers[user.numbers_style] = "✅ " + numbers.get(user.numbers_style, "")

    return {"game_numbers": list(getter_numbers.values())}


async def show_confirmation(_call: CallbackQuery, button: Button, manager: DialogManager):
    state = manager.current_context().state.state.split(":")[-1]
    session = manager.data.get("session")
    user: User = await session.get(User, _call.from_user.id)
    dialog_data = manager.current_context().dialog_data

    if button.widget_id in (user.theme, user.controllers, user.numbers_style):
        pop_no_need_data(dialog_data)
        return

    if state == "theme":
        dialog_data["new_theme"] = button.widget_id

    elif state == "controllers":
        dialog_data["new_controllers"] = button.widget_id

    elif state == "numbers":
        dialog_data["new_number_style"] = button.widget_id


async def change_game_settings(call: CallbackQuery, _button: Button, manager: DialogManager):
    state = manager.current_context().state.state.split(":")[-1]
    session = manager.data.get("session")
    user: User = await session.get(User, call.from_user.id)
    dialog_data = manager.current_context().dialog_data

    if state == "theme":
        user.theme = dialog_data.get("new_theme")

    elif state == "controllers":
        user.controllers = dialog_data.get("new_controllers")

    elif state == "numbers":
        user.numbers_style = dialog_data.get("new_number_style")

    await session.commit()
    pop_no_need_data(dialog_data)

    await call.answer(f"⚡️ The {state} of the game has been changed!")


def pop_no_need_data(dialog_data):
    dialog_data.pop("new_theme", None)
    dialog_data.pop("new_controllers", None)
    dialog_data.pop("new_number_style", None)


async def clear_data(_call: CallbackQuery, _button: Button, manager: DialogManager):
    dialog_data = manager.current_context().dialog_data
    pop_no_need_data(dialog_data)

settings_dialog = Dialog(
    Window(
        Const("Select the desired section:"),
        Column(
            Next(text=Const("🧑‍🎤 Theme")),
            SwitchTo(
                text=Const("🕹 Controllers"),
                id="controllers",
                state=Settings.controllers
            ),
            SwitchTo(
                text=Const("🔢 Numbers style"),
                id="nums_style",
                state=Settings.numbers
            ),
            Start(
                text=Const("🔙 Back"),
                id="to_main",
                state=Main.main,
                mode=StartMode.RESET_STACK
            ),
        ),
        state=Settings.main
    ),
    Window(
        DynamicMediaFileId(
            file_id=Format(text='{photo_theme}'), when="photo_theme"
        ),
        Format(text="{theme_text}", when="theme_text"),
        Column(
            Button(
                text=Format(text="{game_themes[0]}"),
                id=CLASSIC_THEME,
                on_click=show_confirmation
            ),
            Button(
                text=Format(text="{game_themes[1]}"),
                id=VITALII_THEME,
                on_click=show_confirmation
            )
        ),
        Row(
            Button(
                text=Const("❌ No"),
                id="cancel",
                on_click=clear_data
            ),
            Button(
                text=Const("✅ Yes"),
                id="yes",
                on_click=change_game_settings
            ),
            when="confirm_theme"
        ),
        SwitchTo(
            text=Const("🔙 Back"),
            id="back",
            state=Settings.main,
            on_click=clear_data
        ),
        state=Settings.theme,
        getter=[get_themes, get_theme_text]
    ),

    Window(
        DynamicMediaFileId(
            file_id=Format(text='{photo_controllers}'), when="photo_controllers"
        ),
        Format(text="{controllers_text}", when="controllers_text"),
        Column(
            Button(
                text=Format(text="{game_controllers[0]}"),
                id=CLASSIC_CONTROLLERS,
                on_click=show_confirmation
            ),
            Button(
                text=Format(text="{game_controllers[1]}"),
                id=VITALII_CONTROLLERS,
                on_click=show_confirmation
            ),
            Button(
                text=Format(text="{game_controllers[2]}"),
                id=MILL_CONTROLLERS,
                on_click=show_confirmation
            )
        ),
        Row(
            Button(
                text=Const("❌ No"),
                id="cancel",
                on_click=clear_data
            ),
            Button(
                text=Const("✅ Yes"),
                id="yes",
                on_click=change_game_settings
            ),
            when="confirm_controllers"
        ),
        SwitchTo(
            text=Const("🔙 Back"),
            id="back",
            state=Settings.main,
            on_click=clear_data
        ),
        state=Settings.controllers,
        getter=[get_controllers, get_controllers_text]
    ),

    Window(
        DynamicMediaFileId(
            file_id=Format(text='{photo_numbers}'), when="photo_numbers"
        ),
        Format(text="{numbers_text}", when="numbers_text"),
        Column(
            Button(
                text=Format(text="{game_numbers[0]}"),
                id=CLASSIC_NUMBERS,
                on_click=show_confirmation
            ),
            Button(
                text=Format(text="{game_numbers[1]}"),
                id=EMOJI_NUMBERS,
                on_click=show_confirmation
            ),
            Button(
                text=Format(text="{game_numbers[2]}"),
                id=ROMAN_NUMBERS,
                on_click=show_confirmation
            )
        ),
        Row(
            Button(
                text=Const("❌ No"),
                id="cancel",
                on_click=clear_data
            ),
            Button(
                text=Const("✅ Yes"),
                id="yes",
                on_click=change_game_settings
            ),
            when="confirm_numbers"
        ),
        SwitchTo(
            text=Const("🔙 Back"),
            id="back",
            state=Settings.main,
            on_click=clear_data
        ),
        state=Settings.numbers,
        getter=[get_numbers, get_numbers_text]
    )
)
