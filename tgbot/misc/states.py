from aiogram.dispatcher.filters.state import StatesGroup, State


class Main(StatesGroup):
    main = State()
    statistics = State()


class Game(StatesGroup):
    on = State()
