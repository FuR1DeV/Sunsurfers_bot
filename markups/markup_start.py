from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

inline_start = InlineKeyboardMarkup()
markup_clean = ReplyKeyboardRemove()

start_1 = InlineKeyboardButton(text='ОММММММММ',
                               callback_data='om')
inline_start.insert(start_1)

