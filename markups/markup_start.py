from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton


markup_clean = ReplyKeyboardRemove()


def send_my_geo():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton(text='Отправить моё местоположение', request_location=True)
    keyboard.add(button)
    return keyboard


def start():
    inline_start = InlineKeyboardMarkup()
    start_1 = InlineKeyboardButton(text='Enter bot',
                                   callback_data='enter_bot')
    inline_start.insert(start_1)
    return inline_start
