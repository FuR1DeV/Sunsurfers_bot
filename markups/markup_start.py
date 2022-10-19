from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton

from settings import config

markup_clean = ReplyKeyboardRemove()


def send_my_geo():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text='Submit my location', request_location=True)
    keyboard.add(button)
    return keyboard


def start():
    inline_start = InlineKeyboardMarkup()
    start_1 = InlineKeyboardButton(text=f'{config.KEYBOARD.get("RIGHT_ARROW")} Enter bot {config.KEYBOARD.get("LEFT_ARROW")}',
                                   callback_data='enter_bot')
    inline_start.insert(start_1)
    return inline_start


def start_menu():
    inline_start = InlineKeyboardMarkup()
    start_1 = InlineKeyboardButton(text=f'{config.KEYBOARD.get("RIGHT_ARROW")} Enter Main Menu {config.KEYBOARD.get("LEFT_ARROW")}',
                                   callback_data='enter_menu')
    inline_start.insert(start_1)
    return inline_start


def update_location():
    inline_update = InlineKeyboardMarkup()
    start_1 = InlineKeyboardButton(text=f'{config.KEYBOARD.get("UP!_BUTTON")} Update My Location {config.KEYBOARD.get("UP!_BUTTON")}',
                                   callback_data='update_location')
    inline_update.insert(start_1)
    return inline_update


def update_location_send_my_geo():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    back = KeyboardButton(text=f'{config.KEYBOARD.get("RIGHT_ARROW_CURVING_LEFT")} Back')
    button = KeyboardButton(text='Update my location', request_location=True)
    keyboard.add(button)
    keyboard.add(back)
    return keyboard
