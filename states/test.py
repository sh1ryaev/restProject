from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    test1 = State()
    test2 = State()
    test3 = State()


class MyInfo(StatesGroup):
    test1 = State()
    test2 = State()
    test3 = State()


class DoOrder(StatesGroup):
    test1 = State()
    test2 = State()
    test3 = State()