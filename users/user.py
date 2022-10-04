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
            button = types.KeyboardButton(text='Phone request', request_contact=True)
            keyboard.add(button)
            await bot.send_message(callback.from_user.id,
                                   f"{callback.from_user.first_name}\n"
                                   f"Share with us your phone number!",
                                   reply_markup=keyboard)
            await states.UserPhone.phone.set()
        elif not user_get_db_obj.user_ban(callback.from_user.id)[0]:
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await states.UserStart.user_menu.set()
            await bot.send_message(callback.from_user.id,
                                   "Thank you for using our bot!",
                                   reply_markup=markup_users.main_menu())
        else:
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await bot.send_message(callback.from_user.id, "You are blocked! Contact technical support!")

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
                                   f"{message.from_user.first_name} In order to use this bot you must "
                                   f"provide information about your location",
                                   reply_markup=markup_start.send_my_geo())
            await states.UserStart.geo.set()
        else:
            await bot.send_message(message.from_user.id,
                                   "This is not your phone number!\n"
                                   "Press /start to start again")

    @staticmethod
    async def geo_position(message: types.Message, state: FSMContext):
        try:
            n = Nominatim(user_agent='User')
            loc = f"{message.location.latitude}, {message.location.longitude}"
            location = n.reverse(loc)
            country = location.raw.get("address").get("country")
            state_ = location.raw.get("address").get("state")
            city = location.raw.get("address").get("city")
            address = f'{location.raw.get("address").get("road")} - {location.raw.get("address").get("house_number")}'
            latitude = location.raw.get("lat")
            longitude = location.raw.get("lon")
            if city is None:
                city = location.raw.get("address").get("town")
            await bot.send_message(message.from_user.id,
                                   f'Country: {country}\n'
                                   f'State: {state_}\n'
                                   f'City: {city}\n'
                                   f'Address: {address}\n')
            await bot.send_message(message.from_user.id,
                                   "Please check the coordinates, if you made a mistake, "
                                   "you can send the geolocation again. If everything is ok, "
                                   "click OK",
                                   reply_markup=markup_start.start())
            user_set_db_obj.user_set_geo(
                message.from_user.id, country, state_, city, address, latitude, longitude)
        except AttributeError:
            await bot.send_message(message.from_user.id,
                                   "Something went wrong, contact support")
        await state.finish()

    @staticmethod
    async def main(message: types.Message):
        await bot.send_message(message.from_user.id,
                               f"{message.from_user.first_name} You are in the main menu",
                               reply_markup=markup_users.main_menu())
        await states.UserStart.user_menu.set()

    @staticmethod
    async def user_menu(message: types.Message, state: FSMContext):
        await state.finish()
        if "My profile" in message.text:
            UserProfile.register_user_profile(dp)
            res = user_get_db_obj.user_exists(message.from_user.id)
            await states.UserProfile.my_profile.set()
            await bot.send_message(message.from_user.id,
                                   f"{config.KEYBOARD.get('DASH') * 14}\n"
                                   f"Your Profile:\n"
                                   f"{config.KEYBOARD.get('ID_BUTTON')} "
                                   f"Your ID: <b>{message.from_user.id}</b>\n"
                                   f"{config.KEYBOARD.get('BUST_IN_SILHOUETTE')} "
                                   f"Your nickname <b>@{message.from_user.username}</b>\n"
                                   f"{config.KEYBOARD.get('TELEPHONE')} "
                                   f"Your number <b>{res[3]}</b>\n"
                                   f"{config.KEYBOARD.get('INFORMATION')} "
                                   f"Your Country <b>{res[7]}</b>\n"
                                   f"{config.KEYBOARD.get('INFORMATION')} "
                                   f"Your State <b>{res[8]}</b>\n"
                                   f"{config.KEYBOARD.get('INFORMATION')} "
                                   f"Your City <b>{res[9]}</b>\n"
                                   f"{config.KEYBOARD.get('INFORMATION')} "
                                   f"Your Address <b>{res[10]}</b>\n"
                                   f"{config.KEYBOARD.get('DASH') * 14}",
                                   reply_markup=markup_users.user_profile())
        # if "Информация" in message.text:
        #     CustomerCreateTask.register_customer_create_task(dp)
        #     await customer_states.CustomerCreateTask.create.set()
        #     await bot.send_message(message.from_user.id,
        #                            "Хотите создать новый заказ ?",
        #                            reply_markup=markup_customer.approve())
        # if "Обратная связь" in message.text:
        #     await customer_states.CustomerHelp.help.set()
        #     await bot.send_message(message.from_user.id,
        #                            "Опишите вашу проблему, можете прикрепить фото или видео\n"
        #                            "Когда закончите сможете вернуться в главное меню",
        #                            reply_markup=markup_customer.photo_or_video_help())
        #     CustomerHelp.register_customer_help(dp)

    @staticmethod
    def register_user_handler(dp: Dispatcher):
        dp.register_message_handler(UserMain.phone, content_types=['contact'],
                                    state=states.UserPhone.phone)
        dp.register_callback_query_handler(UserMain.hi_user, text='enter_bot')
        dp.register_message_handler(UserMain.geo_position, content_types=['location', 'text'], state=states.UserStart.geo)
        dp.register_message_handler(UserMain.main, state=states.UserStart.start)
        dp.register_message_handler(UserMain.user_menu, state=states.UserStart.user_menu)


class UserProfile:
    @staticmethod
    async def user_profile(message: types.Message):
        if message.text == "Main menu":
            await states.UserStart.user_menu.set()
            await bot.send_message(message.from_user.id,
                                   "You have returned to the main menu",
                                   reply_markup=markup_users.main_menu(),
                                   )
        if message.text == "Update Location":
            await bot.send_message(message.from_user.id,
                                   "This is where your location update will be implemented")

    @staticmethod
    def register_user_profile(dp):
        dp.register_message_handler(UserProfile.user_profile,
                                    state=states.UserProfile.my_profile)

