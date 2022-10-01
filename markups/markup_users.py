from aiogram import types
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

markup_clean = ReplyKeyboardRemove()


def back():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Назад")
    return keyboard


def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Мой профиль", "Информация")
    keyboard.row("Обратная связь")
    return keyboard

