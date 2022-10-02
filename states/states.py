from aiogram.dispatcher.filters.state import State, StatesGroup


class UserPhone(StatesGroup):
    phone: State = State()


class UserStart(StatesGroup):
    start: State = State()
    user_menu: State = State()


class UserProfile(StatesGroup):
    my_profile: State = State()
