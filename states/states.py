from aiogram.dispatcher.filters.state import State, StatesGroup


class UserPhone(StatesGroup):
    phone: State = State()


class UserStart(StatesGroup):
    geo: State = State()
    start: State = State()
    user_menu: State = State()


class UserProfile(StatesGroup):
    my_profile: State = State()
    update_location: State = State()
    about_me: State = State()


class Information(StatesGroup):
    info: State = State()
    user_info: State = State()


class Sun(StatesGroup):
    sun_menu: State = State()
    country_menu: State = State()
    about: State = State()


class Services(StatesGroup):
    start: State = State()
    help: State = State()
    om: State = State()
