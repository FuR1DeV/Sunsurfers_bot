from aiogram.dispatcher.filters.state import State, StatesGroup


class UserPhone(StatesGroup):
    phone: State = State()


class UserStart(StatesGroup):
    geo: State = State()
    start: State = State()
    user_menu: State = State()


class UserProfile(StatesGroup):
    my_profile: State = State()
    update_info: State = State()
    update_location: State = State()
    update_about_me: State = State()
    update_first_name: State = State()
    update_last_name: State = State()


class Information(StatesGroup):
    info: State = State()
    user_info: State = State()


class Sun(StatesGroup):
    sun_menu: State = State()
    country_menu: State = State()
    about: State = State()


class Projects(StatesGroup):
    start: State = State()
    help: State = State()
    marathons: State = State()
