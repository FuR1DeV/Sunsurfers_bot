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
    keyboard.row(f"{config.KEYBOARD.get('WRENCH')} Projects",
                 f"{config.KEYBOARD.get('SUN')} Events")
    return keyboard


def user_profile():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('UP!_BUTTON')} Update Information",
                 f"{config.KEYBOARD.get('SMILING_FACE_WITH_SUNGLASSES')} About me")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def user_profile_update_info():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('WORLD_MAP')} Update Location",
                 f"{config.KEYBOARD.get('CLIPBOARD')} Update About me")
    keyboard.row(f"{config.KEYBOARD.get('INFORMATION')} Update First Name",
                 f"{config.KEYBOARD.get('INFORMATION')} Update Last Name")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back")
    return keyboard


def user_feedback():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back")
    return keyboard


def projects():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('FOLDED_HANDS')} Marathons",
                 f"{config.KEYBOARD.get('FOLDED_HANDS')} SunSchool")
    keyboard.row(f"{config.KEYBOARD.get('FOLDED_HANDS')} Travel Book",
                 f"{config.KEYBOARD.get('FOLDED_HANDS')} Ecovillage in Georgia",
                 f"{config.KEYBOARD.get('SOS_BUTTON')} Feedback")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def marathons():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('FOLDED_HANDS')} Yoga marathon",
                 f"{config.KEYBOARD.get('FOLDED_HANDS')} Interval training marathon")
    keyboard.row(f"{config.KEYBOARD.get('FOLDED_HANDS')} Marathon of minimalism",
                 f"{config.KEYBOARD.get('FOLDED_HANDS')} Marathon of early rises")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back")
    return keyboard


def sun_gathering_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('SUN')} SunGathering",
                 f"{config.KEYBOARD.get('SUN')} SunUniversity",
                 f"{config.KEYBOARD.get('SUN')} SunAtorium",)
    keyboard.row(f"{config.KEYBOARD.get('SUN')} Yoga Retreat",
                 f"{config.KEYBOARD.get('SUN')} SunWomanCamp",
                 f"{config.KEYBOARD.get('SUN')} Meetups")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def sun_gathering_menu_select_country(user_exists):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if user_exists:
        keyboard.row(f"{config.KEYBOARD.get('SUNRISE')} About SunGathering",
                     f"{config.KEYBOARD.get('CLIPBOARD')} My words about SunGathering")
        keyboard.row(f"{config.KEYBOARD.get('EX_QUEST_MARK')} Who was there?")
    else:
        keyboard.row(f"{config.KEYBOARD.get('SUNRISE')} About SunGathering",
                     f"{config.KEYBOARD.get('WAVING_HAND')} I was there!")
        keyboard.row(f"{config.KEYBOARD.get('EX_QUEST_MARK')} Who was there?")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def user_choose():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('CLIPBOARD')} About him/her",
                 f"{config.KEYBOARD.get('SUN')} Words about SunGatherings")
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Main menu")
    return keyboard


def about_sun_gathering():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(f"{config.KEYBOARD.get('RIGHT_ARROW_CURVING_LEFT')} Back")
    return keyboard


def add_event():
    inline_add = InlineKeyboardMarkup()
    add = InlineKeyboardButton(text='Add to this event', callback_data='add_to_event')
    inline_add.insert(add)
    return inline_add
