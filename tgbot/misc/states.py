from aiogram.dispatcher.filters.state import StatesGroup, State


class Main(StatesGroup):
    main = State()
    new_game = State()
    statistics = State()


class Game(StatesGroup):
    on = State()


class Leaderboard(StatesGroup):
    main = State()


class MyGameHistory(StatesGroup):
    main = State()


class Settings(StatesGroup):
    main = State()
    theme = State()
    controllers = State()
    numbers = State()
