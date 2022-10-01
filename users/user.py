import logging
from datetime import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from geopy.geocoders import Nominatim

from bot import bot, dp
from data.get_set_db import global_get_db_obj, user_get_db_obj, user_set_db_obj
from markups import markup_start, markup_users
from settings import config
from states import states


class UserMain:
    @staticmethod
    async def hi_user(callback: types.CallbackQuery):
        if not user_get_db_obj.user_exists(callback.from_user.id):
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            button = types.KeyboardButton(text='Запрос телефона', request_contact=True)
            keyboard.add(button)
            await bot.send_message(callback.from_user.id,
                                   f"{callback.from_user.first_name}\n"
                                   f"Поделитесь с нами вашим номером телефона!",
                                   reply_markup=keyboard)
            await states.UserPhone.phone.set()
        elif not user_get_db_obj.user_ban(callback.from_user.id)[0]:
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await states.UserStart.user_menu.set()
            await bot.send_message(callback.from_user.id,
                                   "Спасибо что пользуетесь нашим ботом!",
                                   reply_markup=markup_users.main_menu())
        else:
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await bot.send_message(callback.from_user.id, "Вы заблокированы! Обратитесь в техподдержку!")

    @staticmethod
    async def phone(message: types.Message):
        if message.contact.user_id == message.from_user.id:
            user_set_db_obj.user_add(message.from_user.id,
                                     message.from_user.username,
                                     message.contact.phone_number,
                                     message.from_user.first_name,
                                     message.from_user.last_name)
            await states.UserStart.user_menu.set()
            await bot.send_message(message.from_user.id,
                                   f"{message.from_user.first_name} Спасибо что пользуетесь нашим ботом!",
                                   reply_markup=markup_users.main_menu())
        else:
            await bot.send_message(message.from_user.id,
                                   "Это не ваш номер телефона! \n"
                                   "Нажмите /start чтобы начать заново")

    @staticmethod
    async def main(message: types.Message):
        await bot.send_message(message.from_user.id,
                               f"{message.from_user.first_name} Вы в главном меню",
                               reply_markup=markup_users.main_menu())
        await states.UserStart.user_menu.set()

    # @staticmethod
    # async def user_menu(message: types.Message, state: FSMContext):
    #     await state.finish()
    #     if "Мой профиль" in message.text:
    #         CustomerProfile.register_customer_profile(dp)
    #         phone_number = customer_get_db_obj.customer_exists(message.from_user.id)[3]
    #         await customer_states.CustomerProfile.my_profile.set()
    #         await bot.send_message(message.from_user.id,
    #                                f"{config.KEYBOARD.get('DASH') * 14}\n"
    #                                f"Ваш профиль <b>Заказчика</b>:\n"
    #                                f"{config.KEYBOARD.get('ID_BUTTON')} "
    #                                f"Ваш ID: <b>{message.from_user.id}</b>\n"
    #                                f"{config.KEYBOARD.get('BUST_IN_SILHOUETTE')} "
    #                                f"Ваш никнейм <b>@{message.from_user.username}</b>\n"
    #                                f"{config.KEYBOARD.get('TELEPHONE')} "
    #                                f"Ваш номер <b>{phone_number}</b>\n"
    #                                f"{config.KEYBOARD.get('DOLLAR')} "
    #                                f"Ваш текущий баланс "
    #                                f"<b>{customer_get_db_obj.customer_money(message.from_user.id)[0]}"
    #                                f"</b> руб.\n{config.KEYBOARD.get('BAR_CHART')} "
    #                                f"Ваш рейтинг <b>"
    #                                f"{str(customer_get_db_obj.customer_rating(message.from_user.id)[0])[0:5]}</b>\n"
    #                                f"{config.KEYBOARD.get('DASH') * 14}",
    #                                reply_markup=markup_customer.customer_profile())
    #     if "Информация" in message.text:
    #         CustomerCreateTask.register_customer_create_task(dp)
    #         await customer_states.CustomerCreateTask.create.set()
    #         await bot.send_message(message.from_user.id,
    #                                "Хотите создать новый заказ ?",
    #                                reply_markup=markup_customer.approve())
    #     if "Обратная связь" in message.text:
    #         await customer_states.CustomerHelp.help.set()
    #         await bot.send_message(message.from_user.id,
    #                                "Опишите вашу проблему, можете прикрепить фото или видео\n"
    #                                "Когда закончите сможете вернуться в главное меню",
    #                                reply_markup=markup_customer.photo_or_video_help())
    #         CustomerHelp.register_customer_help(dp)

    @staticmethod
    def register_user_handler(dp: Dispatcher):
        dp.register_message_handler(UserMain.phone, content_types=['contact'],
                                    state=states.UserPhone.phone)
        dp.register_callback_query_handler(UserMain.hi_user, text='om')
        dp.register_message_handler(UserMain.main, state=states.UserStart.start)
        # dp.register_message_handler(UserMain.user_menu, state=states.UserStart.user_menu)
