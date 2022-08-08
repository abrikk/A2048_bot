import operator

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Select, Group, Row
from aiogram_dialog.widgets.text import Format

from tgbot.handlers.game.getters import set_random_fields, get_game_data, move_numbers
from tgbot.handlers.game.logic import when_not
from tgbot.misc.states import Game

game_dialog = Dialog(
    Window(
        Format(text="{game_text}", when="game_text"),

        Group(
            Row(
                Select(
                    Format("{item[1]}"),
                    id="line_1_field",
                    item_id_getter=operator.itemgetter(0),
                    items="fields_1",
                )
            ),

            Row(
                Select(
                    Format("{item[1]}"),
                    id="line_2_field",
                    item_id_getter=operator.itemgetter(0),
                    items="fields_2",
                )
            ),

            Row(
                Select(
                    Format("{item[1]}"),
                    id="line_3_field",
                    item_id_getter=operator.itemgetter(0),
                    items="fields_3",
                )
            ),

            Row(
                Select(
                    Format("{item[1]}"),
                    id="line_4_field",
                    item_id_getter=operator.itemgetter(0),
                    items="fields_4",
                )
            ),

            Row(
                Select(
                    Format("{item[1]}"),
                    id="line_5_field",
                    item_id_getter=operator.itemgetter(0),
                    items="fields_5",
                ),
                when=lambda data, widget, manager: data.get("start_data", {}).get("board_size") >= 5
            ),

            Row(
                Select(
                    Format("{item[1]}"),
                    id="line_6_field",
                    item_id_getter=operator.itemgetter(0),
                    items="fields_6",
                ),
                when=lambda data, widget, manager: data.get("start_data", {}).get("board_size") >= 6
            ),

            Row(
                Select(
                    Format("{item[1]}"),
                    id="line_7_field",
                    item_id_getter=operator.itemgetter(0),
                    items="fields_7",
                ),
                when=lambda data, widget, manager: data.get("start_data", {}).get("board_size") >= 7
            ),
            when="classic_theme",
            id="board"
        ),
        Group(
            Row(
                Select(
                    Format("{item[1]}"),
                    id="direction",
                    item_id_getter=operator.itemgetter(0),
                    items="first_line",
                    on_click=move_numbers
                ),
            ),
            Row(
                Select(
                    Format("{item[1]}"),
                    id="direction",
                    item_id_getter=operator.itemgetter(0),
                    items="second_line",
                    on_click=move_numbers
                ),
            ),
            Row(
                Select(
                    Format("{item[1]}"),
                    id="direction",
                    item_id_getter=operator.itemgetter(0),
                    items="third_line",
                    on_click=move_numbers
                ),
                when="third_line"
            ),

            id="controllers",
            when=when_not("game_over")
        ),
        state=Game.on,
        getter=get_game_data
    ),
    on_start=set_random_fields
)
