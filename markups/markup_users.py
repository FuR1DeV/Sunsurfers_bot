from aiogram import types
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from settings import config

markup_clean = ReplyKeyboardRemove()


def back():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back")
    return keyboard


def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('BUST_IN_SILHOUETTE')} My profile",
                 f"{config.KEYBOARD.get('WORLD_MAP')} Locations")
    keyboard.row(f"{config.KEYBOARD.get('WRENCH')} Services",
                 f"{config.KEYBOARD.get('SUN')} SunGatherings")
    return keyboard


def user_profile():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('WORLD_MAP')} Update Location",
                 f"{config.KEYBOARD.get('CLIPBOARD')} Update About me")
    keyboard.row(f"{config.KEYBOARD.get('SMILING_FACE_WITH_SUNGLASSES')} About me")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def user_feedback():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back")
    return keyboard


def user_om():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('NAZAR_AMULET')} Human Design")
    keyboard.row(f"{config.KEYBOARD.get('YIN_YANG')} Gene Keys")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back")
    return keyboard


def services():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('FOLDED_HANDS')} OM",
                 f"{config.KEYBOARD.get('SOS_BUTTON')} Feedback")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def sun_gathering_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('SUN')} Choose SunGathering",
                 f"{config.KEYBOARD.get('SUN')} Choose SunUniversity")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def sun_gathering_menu_select_country(user_exists):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('SUNRISE')} About SunGathering",
                 f"{config.KEYBOARD.get('WAVING_HAND')} I was there!")
    if user_exists:
        keyboard.row(f"{config.KEYBOARD.get('CLIPBOARD')} My words about SunGathering")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def user_choose():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('CLIPBOARD')} About him/her")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def about_sun_gathering():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('CROSS_MARK')} Cancel")
    return keyboard


def add_event():
    inline_add = InlineKeyboardMarkup()
    add = InlineKeyboardButton(text='Add to this event', callback_data='add_to_event')
    inline_add.insert(add)
    return inline_add
