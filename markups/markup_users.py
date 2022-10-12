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
    keyboard.row(f"{config.KEYBOARD.get('OM')} OM",
                 f"{config.KEYBOARD.get('SUN')} SunGatherings")
    keyboard.row(f"{config.KEYBOARD.get('SOS_BUTTON')} Feedback")
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
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def user_om():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('NAZAR_AMULET')} Human Design")
    keyboard.row(f"{config.KEYBOARD.get('YIN_YANG')} Gene Keys")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def sun_gathering_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('SUN')} Choose SunGathering",
                 f"{config.KEYBOARD.get('SUN')} Choose SunUniversity")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def user_choose():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('CLIPBOARD')} About him/her")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def go_info():
    inline_go = InlineKeyboardMarkup()
    go = InlineKeyboardButton(text='GO', callback_data='go_info')
    inline_go.insert(go)
    return inline_go


def sun_gathering():

    return inline_go
